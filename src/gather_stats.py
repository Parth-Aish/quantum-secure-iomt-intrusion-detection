import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import joblib

lstm = tf.keras.models.load_model('../results/results_final_leakfree/lstm_model.h5', compile=False)
lstm_params = lstm.count_params()

ocsvm = joblib.load('../results/results_final_leakfree/ocsvm_model.joblib')
n_sv = ocsvm.support_vectors_.shape[0] if hasattr(ocsvm, 'support_vectors_') else len(ocsvm.support_)
print(f"LSTM Params: {lstm_params}")
print(f"OCSVM Support Vectors: {n_sv}")
