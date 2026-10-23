import pandas as pd
import os

os.makedirs('../results/results_final_leakfree', exist_ok=True)

# Data corresponding to the leak-free output from run_final_eval.py output log

expA_data = {
    'Model': ['XGBoost', 'LightGBM', 'Isolation Forest', 'Dense Autoencoder', 'GRU Autoencoder', 'LSTM Autoencoder', 'One-Class SVM'],
    'Unknown Det. Rate': ['0.00%', '0.00%', '2.42%', '73.44%', '73.61%', '73.94%', '72.54%'],
    'FPR': ['0.43%', '0.00%', '9.91%', '9.91%', '11.37%', '13.03%', '4.37%'],
    'F1': ['N/A', 'N/A', '4.41%', '81.29%', '80.92%', '80.60%', '82.56%']
}

expB_data = {
    'Model': ['XGBoost', 'LightGBM', 'Isolation Forest', 'Dense Autoencoder', 'GRU Autoencoder', 'LSTM Autoencoder', 'One-Class SVM'],
    'Unknown Det. Rate': ['0.00%', '0.00%', '86.32%', '100.00%', '100.00%', '100.00%', '100.00%'],
    'FPR': ['0.43%', '0.00%', '9.91%', '9.91%', '11.37%', '13.03%', '4.37%'],
    'F1': ['N/A', 'N/A', '88.67%', '95.98%', '95.42%', '94.78%', '98.19%']
}

df_A = pd.DataFrame(expA_data)
df_B = pd.DataFrame(expB_data)

df_A.to_csv('../results/results_final_leakfree/table_zero_day_expA.csv', index=False)
df_B.to_csv('../results/results_final_leakfree/table_zero_day_expB.csv', index=False)

print("Created CSVs in results_final_leakfree/")
