import os, time
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM
import tensorflow as tf
import joblib
from sklearn.metrics import roc_curve, auc, precision_recall_curve
import matplotlib.pyplot as plt

print("Loading data...")
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
        wX = X_sc[i:i+seq_len]
        wy = 1 if np.sum(y_arr[i:i+seq_len]) > 0 else 0
        if wy == 0: train_w.append(wX.flatten())
    elif i >= train_end and end < val_end:
        pass
    elif i >= val_end:
        wX = X_sc[i:i+seq_len]
        wy = 1 if np.sum(y_arr[i:i+seq_len]) > 0 else 0
        wcats = cat_arr[i:i+seq_len]
        wcat = 'spoofing' if 'spoofing' in wcats else 'data alteration' if 'data alteration' in wcats else 'normal'
        test_w.append(wX)
        test_y.append(wy)
        test_c.append(wcat)

test_w = np.array(test_w)
test_y = np.array(test_y)
test_c = np.array(test_c)
flat_test = test_w.reshape(len(test_w), -1)

print("Training OC-SVM...")
clf_oc = OneClassSVM(kernel='rbf', nu=0.05, gamma='scale')
clf_oc.fit(train_w)
joblib.dump(clf_oc, '../results/results_final_leakfree/ocsvm_model.joblib')
oc_size = os.path.getsize('../results/results_final_leakfree/ocsvm_model.joblib') / (1024*1024)

print("Benchmarking OC-SVM inference...")
start = time.time()
p_oc_scores = clf_oc.decision_function(flat_test)
# In sklearn OC-SVM, positive score = inlier (normal), negative score = outlier (anomaly)
# We want anomaly scores where higher is more anomalous for ROC.
anomaly_scores = -p_oc_scores
end = time.time()
oc_latency = ((end - start) / len(test_w)) * 1000

print("Benchmarking LSTM inference...")
lstm = tf.keras.models.load_model('../results/results_final_leakfree/lstm_model.h5', compile=False)
start = time.time()
test_pred = lstm.predict(test_w, batch_size=128, verbose=0)
end = time.time()
lstm_latency = ((end - start) / len(test_w)) * 1000
lstm_size = os.path.getsize('../results/results_final_leakfree/lstm_model.h5') / (1024*1024)

# Create ROC Curve for OC-SVM
os.makedirs('figures_leakfree', exist_ok=True)
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)

# Exp A (Spoofing)
maskA = (test_c == 'normal') | (test_c == 'spoofing')
fprA, tprA, _ = roc_curve(test_y[maskA], anomaly_scores[maskA])
roc_aucA = auc(fprA, tprA)
plt.plot(fprA, tprA, lw=2, label=f'Spoofing (AUC = {roc_aucA:.3f})')

# Exp B (Data Alteration)
maskB = (test_c == 'normal') | (test_c == 'data alteration')
fprB, tprB, _ = roc_curve(test_y[maskB], anomaly_scores[maskB])
roc_aucB = auc(fprB, tprB)
plt.plot(fprB, tprB, lw=2, label=f'Data Alt (AUC = {roc_aucB:.3f})')

plt.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve (OC-SVM)')
plt.legend(loc="lower right")
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
# Exp A PR
precA, recA, _ = precision_recall_curve(test_y[maskA], anomaly_scores[maskA])
plt.plot(recA, precA, lw=2, label=f'Spoofing')
# Exp B PR
precB, recB, _ = precision_recall_curve(test_y[maskB], anomaly_scores[maskB])
plt.plot(recB, precB, lw=2, label=f'Data Alt')

plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve (OC-SVM)')
plt.legend(loc="lower left")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures_leakfree/fig4_pr_roc_curves.png', dpi=300)
plt.close()

with open('../results/results_final_leakfree/benchmarks.txt', 'w') as f:
    f.write(f"OC-SVM Size: {oc_size:.4f} MB\n")
    f.write(f"OC-SVM Latency: {oc_latency:.4f} ms/window\n")
    f.write(f"LSTM Size: {lstm_size:.4f} MB\n")
    f.write(f"LSTM Latency: {lstm_latency:.4f} ms/window\n")

print(f"OC-SVM: {oc_size:.4f} MB, {oc_latency:.4f} ms")
print(f"LSTM: {lstm_size:.4f} MB, {lstm_latency:.4f} ms")
