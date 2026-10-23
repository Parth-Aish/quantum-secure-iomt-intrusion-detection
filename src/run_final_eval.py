import os, sys, time, json
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score, precision_score, recall_score
from scipy.stats import chi2
import xgboost as xgb
from lightgbm import LGBMClassifier

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

OUTDIR = '../results/results_final_leakfree'
os.makedirs(OUTDIR, exist_ok=True)

print("="*50)
print("1. LOADING & CHRONOLOGICAL PREPROCESSING")
print("="*50)

df = pd.read_csv('../data/wustl-ehms-2020_with_attacks_categories.csv').sort_values('Packet_num').reset_index(drop=True)

def map_cat(c):
    c = str(c).lower()
    if 'spoof' in c: return 'spoofing'
    if 'alter' in c or 'inject' in c: return 'data alteration'
    return 'normal'

df['Cat'] = df['Attack Category'].apply(map_cat)
const_cols = ['Dport', 'SrcGap', 'DstGap', 'DIntPktAct', 'dMinPktSz', 'Trans']
id_cols = ['SrcAddr', 'DstAddr', 'SrcMac', 'DstMac', 'Packet_num', 'Sport']
leak_cols = [c for c in df.columns if 'attack' in c.lower() or c == 'Label' or c == 'Cat']

df_clean = df.drop(columns=[c for c in const_cols + id_cols if c in df.columns])
X_raw = df_clean.drop(columns=[c for c in leak_cols if c in df_clean.columns])
cat_cols = X_raw.select_dtypes(include=['object', 'category']).columns.tolist()
X_encoded = pd.get_dummies(X_raw, columns=cat_cols, drop_first=False)

X_arr = X_encoded.values.astype('float32')
y_arr = df['Label'].values
cat_arr = df['Cat'].values
n_total = len(X_arr)
train_end = int(n_total * 0.70)
val_end = int(n_total * 0.85)

sc = StandardScaler()
sc.fit(X_arr[:train_end][y_arr[:train_end] == 0])
X_sc = sc.transform(X_arr)

seq_len = 30
train_w, val_w, test_w, test_y, test_c = [], [], [], [], []

for i in range(n_total - seq_len + 1):
    end = i + seq_len - 1
    if end < train_end:
        split = 'train'
    elif i >= train_end and end < val_end:
        split = 'val'
    elif i >= val_end:
        split = 'test'
    else:
        continue

    wX = X_sc[i:i+seq_len]
    wy = 1 if np.sum(y_arr[i:i+seq_len]) > 0 else 0
    wcats = cat_arr[i:i+seq_len]
    wcat = 'spoofing' if 'spoofing' in wcats else 'data alteration' if 'data alteration' in wcats else 'normal'

    if split == 'train':
        if wy == 0:
            train_w.append(wX)
        else:
            test_w.append(wX)
            test_y.append(wy)
            test_c.append(wcat)
    elif split == 'val':
        if wy == 0:
            val_w.append(wX)
        else:
            test_w.append(wX)
            test_y.append(wy)
            test_c.append(wcat)
    elif split == 'test':
        test_w.append(wX)
        test_y.append(wy)
        test_c.append(wcat)

train_w = np.array(train_w)
val_w = np.array(val_w)
test_w = np.array(test_w)
test_y = np.array(test_y)
test_c = np.array(test_c)

print(f"Windows -> Train(Normal): {len(train_w)}, Val(Normal): {len(val_w)}, Test(Mixed): {len(test_w)}")
print(f"Test Set Attacks: Spoofing={np.sum(test_c=='spoofing')}, Data Alt={np.sum(test_c=='data alteration')}")

print("\n"+"="*50)
print("2. SUPERVISED BASELINES (XGBoost, LightGBM)")
print("="*50)
# Supervised baselines evaluate rows, preserving chronological train/test splitting.
# Exp A: Known = Data Alt, Unknown = Spoofing
# Exp B: Known = Spoofing, Unknown = Data Alt
def run_supervised(known_cat, unknown_cat):
    # Train = first 70% of rows (normal + known_cat ONLY)
    tr_mask = (np.arange(n_total) < train_end) & ((cat_arr == 'normal') | (cat_arr == known_cat))
    X_tr_sup, y_tr_sup = X_arr[tr_mask], y_arr[tr_mask]

    # Test = Test period rows + all Unknown attacks
    # For fair zero-day evaluation: normal rows from test period + unknown attack rows from anywhere.
    te_mask = ((np.arange(n_total) >= val_end) & (cat_arr == 'normal')) | (cat_arr == unknown_cat)
    X_te_sup, y_te_sup = X_arr[te_mask], y_arr[te_mask]

    # XGBoost
    xgb_clf = xgb.XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')
    xgb_clf.fit(X_tr_sup, y_tr_sup)
    xgb_p = xgb_clf.predict(X_te_sup)
    xgb_tn, xgb_fp, xgb_fn, xgb_tp = confusion_matrix(y_te_sup, xgb_p, labels=[0,1]).ravel()
    xgb_fpr = xgb_fp / (xgb_fp + xgb_tn) if (xgb_fp+xgb_tn)>0 else 0
    xgb_f1 = f1_score(y_te_sup, xgb_p, zero_division=0)

    # LightGBM
    lgb_clf = LGBMClassifier(random_state=42)
    lgb_clf.fit(X_tr_sup, y_tr_sup)
    lgb_p = lgb_clf.predict(X_te_sup)
    lgb_tn, lgb_fp, lgb_fn, lgb_tp = confusion_matrix(y_te_sup, lgb_p, labels=[0,1]).ravel()
    lgb_fpr = lgb_fp / (lgb_fp + lgb_tn) if (lgb_fp+lgb_tn)>0 else 0
    lgb_f1 = f1_score(y_te_sup, lgb_p, zero_division=0)

    print(f"Exp (Unknown={unknown_cat}) - XGBoost: Det={recall_score(y_te_sup, xgb_p):.4f}, FPR={xgb_fpr:.4f}, F1={xgb_f1:.4f}")
    print(f"Exp (Unknown={unknown_cat}) - LightGBM: Det={recall_score(y_te_sup, lgb_p):.4f}, FPR={lgb_fpr:.4f}, F1={lgb_f1:.4f}")

run_supervised('data alteration', 'spoofing')
run_supervised('spoofing', 'data alteration')

print("\n"+"="*50)
print("3. UNSUPERVISED BASELINES (OCSVM, IF, Dense AE, GRU AE)")
print("="*50)
X_tr_f = train_w.reshape(len(train_w), -1)
X_te_f = test_w.reshape(len(test_w), -1)

# OCSVM
oc = OneClassSVM(kernel='rbf', gamma='scale', nu=0.05)
oc.fit(X_tr_f)
p_oc = np.where(oc.predict(X_te_f) == -1, 1, 0)

# IF
iso = IsolationForest(contamination=0.05, random_state=42, n_jobs=-1)
iso.fit(X_tr_f)
p_iso = np.where(iso.predict(X_te_f) == -1, 1, 0)

# Dense AE
inp_d = layers.Input(shape=(X_tr_f.shape[1],))
d = layers.Dense(64, activation='relu')(inp_d)
d = layers.Dense(16, activation='relu')(d)
d = layers.Dense(64, activation='relu')(d)
out_d = layers.Dense(X_tr_f.shape[1])(d)
dense_ae = keras.Model(inp_d, out_d)
dense_ae.compile(optimizer='adam', loss='mse')
dense_ae.fit(X_tr_f, X_tr_f, epochs=50, batch_size=64, validation_split=0.1, callbacks=[keras.callbacks.EarlyStopping(patience=10)], verbose=0)
v_recon_d = dense_ae.predict(val_w.reshape(len(val_w), -1), verbose=0)
th_dense = np.percentile(np.mean((val_w.reshape(len(val_w), -1) - v_recon_d)**2, axis=1), 95)
te_recon_d = dense_ae.predict(X_te_f, verbose=0)
p_dense = (np.mean((X_te_f - te_recon_d)**2, axis=1) > th_dense).astype(int)

# GRU AE
inp_g = layers.Input(shape=(30, train_w.shape[2]))
g = layers.GRU(32, return_sequences=True)(inp_g)
g = layers.GRU(16)(g)
g = layers.RepeatVector(30)(g)
g = layers.GRU(16, return_sequences=True)(g)
g = layers.GRU(32, return_sequences=True)(g)
out_g = layers.TimeDistributed(layers.Dense(train_w.shape[2]))(g)
gru_ae = keras.Model(inp_g, out_g)
gru_ae.compile(optimizer='adam', loss='mse')
gru_ae.fit(train_w, train_w, epochs=50, batch_size=64, validation_data=(val_w, val_w), callbacks=[keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)], verbose=0)
v_recon_g = gru_ae.predict(val_w, verbose=0)
th_gru = np.percentile(np.mean((val_w - v_recon_g)**2, axis=(1,2)), 95)
te_recon_g = gru_ae.predict(test_w, verbose=0)
p_gru = (np.mean((test_w - te_recon_g)**2, axis=(1,2)) > th_gru).astype(int)

print("\n"+"="*50)
print("4. LSTM AE MULTI-SEED ROBUSTNESS & DEPLOYMENT METRICS")
print("="*50)

seeds = [42, 123, 456, 789, 999]
lstm_res_A, lstm_res_B = [], []
p_lstm_42 = None

def build_lstm():
    inp = layers.Input(shape=(30, train_w.shape[2]))
    x = layers.LSTM(32, return_sequences=True)(inp)
    x = layers.LSTM(16)(x)
    b = layers.Dense(8, activation='relu')(x)
    x = layers.RepeatVector(30)(b)
    x = layers.LSTM(16, return_sequences=True)(x)
    x = layers.LSTM(32, return_sequences=True)(x)
    out = layers.TimeDistributed(layers.Dense(train_w.shape[2]))(x)
    return keras.Model(inp, out)

for s in seeds:
    print(f"Training LSTM Seed {s}...")
    np.random.seed(s)
    tf.random.set_seed(s)
    lstm = build_lstm()
    lstm.compile(optimizer='adam', loss='mse')
    t0 = time.time()
    lstm.fit(train_w, train_w, epochs=150, batch_size=64, validation_data=(val_w, val_w), callbacks=[keras.callbacks.EarlyStopping(patience=15, restore_best_weights=True)], verbose=0)

    val_recon = lstm.predict(val_w, verbose=0)
    th_lstm = np.percentile(np.mean((val_w - val_recon)**2, axis=(1,2)), 95)

    te_recon = lstm.predict(test_w, verbose=0)
    p_l = (np.mean((test_w - te_recon)**2, axis=(1,2)) > th_lstm).astype(int)

    if s == 42:
        p_lstm_42 = p_l.copy()
        # Deployment metrics
        lstm.save(os.path.join(OUTDIR, 'lstm_model.h5'))
        size_kb = os.path.getsize(os.path.join(OUTDIR, 'lstm_model.h5')) / 1024
        t_inf_start = time.time()
        lstm.predict(test_w[:100], verbose=0)
        t_inf = (time.time() - t_inf_start) / 100 * 1000 # ms per window
        print(f"  [Deployment] Params: {lstm.count_params()}, Size: {size_kb:.1f} KB, Inf_time: {t_inf:.2f} ms/win")

    def evaluate(p, unknown, known):
        mask = (test_c == 'normal') | (test_c == unknown)
        y_true = test_y[mask]
        y_pred = p[mask]
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0,1]).ravel()
        det = recall_score(y_true, y_pred)
        fpr = fp / (fp + tn) if (fp+tn)>0 else 0
        f1 = f1_score(y_true, y_pred, zero_division=0)
        return det, fpr, f1

    detA, fprA, f1A = evaluate(p_l, 'spoofing', 'data alteration')
    detB, fprB, f1B = evaluate(p_l, 'data alteration', 'spoofing')
    lstm_res_A.append([detA, fprA, f1A])
    lstm_res_B.append([detB, fprB, f1B])

resA = np.array(lstm_res_A) * 100
resB = np.array(lstm_res_B) * 100
print(f"LSTM Exp A (Spoofing): Det={resA[:,0].mean():.2f}±{resA[:,0].std():.2f}%, FPR={resA[:,1].mean():.2f}±{resA[:,1].std():.2f}%, F1={resA[:,2].mean():.2f}±{resA[:,2].std():.2f}%")
print(f"LSTM Exp B (Data Alt): Det={resB[:,0].mean():.2f}±{resB[:,0].std():.2f}%, FPR={resB[:,1].mean():.2f}±{resB[:,1].std():.2f}%, F1={resB[:,2].mean():.2f}±{resB[:,2].std():.2f}%")

print("\n"+"="*50)
print("5. MCNEMAR'S TEST & ZERO-DAY RESULTS (ALL BASELINES)")
print("="*50)
def mcnemar(pA, pB, y):
    cA = (pA == y).astype(int)
    cB = (pB == y).astype(int)
    b01 = ((cA == 0) & (cB == 1)).sum()
    b10 = ((cA == 1) & (cB == 0)).sum()
    if (b01 + b10) == 0: return 0, 1
    stat = (abs(b01 - b10) - 1)**2 / (b01 + b10)
    return stat, 1 - chi2.cdf(stat, 1)

def print_baseline(name, p_baseline):
    # Exp A
    maskA = (test_c == 'normal') | (test_c == 'spoofing')
    y_trueA = test_y[maskA]
    p_bA = p_baseline[maskA]
    detA, fprA, f1A = recall_score(y_trueA, p_bA), confusion_matrix(y_trueA, p_bA, labels=[0,1]).ravel()[1]/sum(test_c=='normal'), f1_score(y_trueA, p_bA, zero_division=0)
    statA, pvalA = mcnemar(p_lstm_42[maskA], p_bA, y_trueA)

    # Exp B
    maskB = (test_c == 'normal') | (test_c == 'data alteration')
    y_trueB = test_y[maskB]
    p_bB = p_baseline[maskB]
    detB, fprB, f1B = recall_score(y_trueB, p_bB), confusion_matrix(y_trueB, p_bB, labels=[0,1]).ravel()[1]/sum(test_c=='normal'), f1_score(y_trueB, p_bB, zero_division=0)
    statB, pvalB = mcnemar(p_lstm_42[maskB], p_bB, y_trueB)

    print(f"[{name}]")
    print(f"  Exp A (Spoofing): Det={detA*100:.2f}%, FPR={fprA*100:.2f}%, F1={f1A*100:.2f}% | McNemar vs LSTM: p={pvalA:.4e}")
    print(f"  Exp B (Data Alt): Det={detB*100:.2f}%, FPR={fprB*100:.2f}%, F1={f1B*100:.2f}% | McNemar vs LSTM: p={pvalB:.4e}")

print_baseline("OC-SVM", p_oc)
print_baseline("Isolation Forest", p_iso)
print_baseline("Dense Autoencoder", p_dense)
print_baseline("GRU Autoencoder", p_gru)

with open(f"{OUTDIR}/completed.txt", "w") as f:
    f.write("All runs completed.")
