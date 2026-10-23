# VERIFIED RESULTS MASTER DOCUMENT
*This document serves as the single source of truth for all project reporting going forward.*

## 1. PIPELINE SOURCE
- **Script:** `run_final_eval.py` (supported by `run_benchmarks.py` for inference latency and `generate_csv.py` for exact tables)
- **Output Directory:** `results_final_leakfree/`
- **Generation Date/Time:** September 25, 2026, ~12:55 PM local time (followed by benchmarks at 1:07 PM).
- **Core Characteristic:** Strict chronological split (70% train, 15% val, 15% test) before windowing, ensuring zero data leakage.

## 2. DISCREPANCY RESOLUTIONS
1. **LSTM Inference Latency:** Previously reported as both 0.84ms and 1.70ms. The final measured latency running strictly over the test set in `run_benchmarks.py` is **4.4790 ms**. Both previous numbers were estimates from varied hardware loads/batch sizes from older pipeline scripts.
2. **QBER Threshold:** Stated as both 10% and 11%. **10%** is now the fixed theoretical limit across all documentation (consistent with the strict BB84 abort thresholds).
3. **Deployment Bounds:** The prior metrics (`<0.10MB`, `<0.50ms`) were theoretical estimates. Actual deployment measurements are now benchmarked and recorded (see Section 5 below).

## 3. ZERO-DAY INTRUSION DETECTION (Experiment A & B)
*Source: `results_final_leakfree/final_results.log`, `results_final_leakfree/table_zero_day_expA.csv`, `results_final_leakfree/table_zero_day_expB.csv`*

### Experiment A (Spoofing - Zero Day)
| Model | Detection Rate | FPR | F1 Score |
|---|---|---|---|
| XGBoost | 0.00% | 0.43% | N/A |
| LightGBM | 0.00% | 0.00% | N/A |
| Isolation Forest | 2.42% | 9.91% | 4.41% |
| Dense Autoencoder | 73.44% | 9.91% | 81.29% |
| GRU Autoencoder | 73.61% | 11.37% | 80.92% |
| LSTM Autoencoder | 73.94% | 13.03% | 80.60% |
| One-Class SVM | 72.54% | 4.37% | 82.56% |

### Experiment B (Data Alteration - Zero Day)
| Model | Detection Rate | FPR | F1 Score |
|---|---|---|---|
| XGBoost | 0.00% | 0.43% | N/A |
| LightGBM | 0.00% | 0.00% | N/A |
| Isolation Forest | 86.32% | 9.91% | 88.67% |
| Dense Autoencoder | 100.00% | 9.91% | 95.98% |
| GRU Autoencoder | 100.00% | 11.37% | 95.42% |
| LSTM Autoencoder | 100.00% | 13.03% | 94.78% |
| One-Class SVM | 100.00% | 4.37% | 98.19% |

## 4. STATISTICAL SIGNIFICANCE (McNemar's Test)
*Source: `task-780.log` (exact script output tracking paired predictions)*
- **Experiment A (OC-SVM vs LSTM):** $\chi^2 = 86.95$, $p < 0.00001$
- **Experiment B (OC-SVM vs LSTM):** $\chi^2 = 110.16$, $p < 0.00001$

## 5. DEPLOYMENT METRICS
*Source: `results_final_leakfree/benchmarks.txt` (via `run_benchmarks.py`) and exact param script (`task-878.log`)*
- **LSTM Autoencoder:**
  - Size: 0.3041 MB (Exact parameters: 21,325 learned weights)
  - Inference Latency: 4.4790 ms
- **One-Class SVM:**
  - Size: 4.7206 MB (Stores exactly 556 support vectors at full 1320-dimensionality)
  - Inference Latency: 1.5115 ms

**Deployment Feasibility Narrative:**
OC-SVM wins decisively on detection performance, FPR, and inference latency (nearly 3x faster than LSTM). However, it LOSES on memory footprint. The 4.72 MB size is because the RBF kernel must store 556 support vectors at full 1320-dimensional window size to compute distances, whereas the LSTM only stores a fixed set of 21,325 parameters.
- *Viability:* A 4.72 MB model is entirely viable for gateway-level edge devices like a Raspberry Pi 4 (which has 2GB-8GB of RAM) or a standard IoT edge node.
- *Constraint:* It would NOT fit on a heavily constrained microcontroller (like an Arduino with <256KB SRAM). This nuance must be corrected in all final reports.

## 6. QUANTUM SECURITY (QKD BB84)
*Source: `src/run_qkd_simulation.py` (extracted standalone BB84 simulation)*
- **No Eavesdropper:** QBER = 0.00%, Key Agreement = 100%
- **Eavesdropper Present:** QBER = ~23.95%, Key Agreement = ~76.05%
- **Abort Threshold:** 10.00%
