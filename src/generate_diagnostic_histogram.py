import os
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

def main():
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
    test_w, test_y, test_c = [], [], []
    for i in range(val_end, n_total - seq_len + 1):
        end = i + seq_len - 1
        test_w.append(X_sc[i:i+seq_len])
        test_y.append(1 if np.any(y_arr[i:i+seq_len]) else 0)

        # Categorize the sequence
        cats = cat_arr[i:i+seq_len]
        if 'spoofing' in cats:
            test_c.append('spoofing')
        elif 'data alteration' in cats:
            test_c.append('data alteration')
        else:
            test_c.append('normal')

    test_w = np.array(test_w)
    test_y = np.array(test_y)
    test_c = np.array(test_c)

    # Filter for Experiment A: Only normal and spoofing
    mask_a = (test_c == 'normal') | (test_c == 'spoofing')
    X_test_A = test_w[mask_a]
    y_test_A = test_y[mask_a]

    # Flatten for OC-SVM
    X_test_A_flat = X_test_A.reshape(X_test_A.shape[0], -1)

    print("Loading OC-SVM model...")
    ocsvm = joblib.load('../results/results_final_leakfree/ocsvm_model.joblib')

    print("Computing decision functions...")
    scores = ocsvm.decision_function(X_test_A_flat)

    # Plot histogram
    plt.figure(figsize=(10, 6))

    scores_normal = scores[y_test_A == 0]
    scores_spoof = scores[y_test_A == 1]

    # Use 100 bins for granularity
    plt.hist(scores_normal, bins=100, color='blue', alpha=0.5, label='Normal Traffic')
    plt.hist(scores_spoof, bins=100, color='red', alpha=0.5, label='Spoofing Attack')

    plt.axvline(x=0, color='black', linestyle='--', linewidth=2, label='Classification Threshold (0.0)')

    plt.title('OC-SVM Decision Margin Distribution (Exp A: Spoofing)')
    plt.xlabel('Decision Function Margin Score')
    plt.ylabel('Frequency')
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)

    out_path = '../results/results_final_leakfree/ocsvm_spoofing_histogram.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"Saved diagnostic plot to {out_path}")

if __name__ == "__main__":
    main()
