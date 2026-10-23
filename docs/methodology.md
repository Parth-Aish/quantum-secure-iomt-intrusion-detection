# Implemented methodology and validity notes

This document follows the code in `src/run_final_eval.py`, not the earlier
topology-aware-attention proposal or idealized system descriptions.

## Data preparation

The script sorts records by `Packet_num`, maps `Attack Category` to normal,
spoofing, or data alteration, removes selected constant/identifier/label
columns, one-hot encodes remaining categorical columns, and standardizes
features. The scaler is fit using normal examples in the first 70% of sorted
rows. Sequence windows have length 30 and do not cross the train/validation/
test boundaries.

The code does **not** fit the one-hot encoder on the training partition alone:
`pandas.get_dummies` runs before the chronological split. The input feature
vocabulary can therefore contain categories first observed later in the data.
This is a preprocessing look-ahead and should be addressed before describing
the pipeline as fully leakage-free.

## Model training and zero-day experiments

- The first 70% of rows is the training period and the next 15% the validation
  period; the final 15% is the chronological test period.
- Unsupervised models are fitted on normal training windows. Autoencoder
  reconstruction thresholds use the 95th percentile of normal validation
  reconstruction errors. One-Class SVM uses `nu=0.05` and its built-in
  decision boundary (zero); it does not use the validation percentile
  threshold.
- Supervised baselines train on normal rows plus the designated known attack
  category.
- Category-specific reports compare normal traffic with one attack category at
  a time.

There is a significant qualification to the time-horizon interpretation:
`run_final_eval.py` appends attack windows from the training and validation
periods to the `test_w` collection, while retaining normal validation windows
only for thresholding. Supervised testing also includes withheld-category
attack rows from any chronological period, as indicated in its test mask.
Consequently the reported attack metrics evaluate withheld attack categories
pooled across periods, not solely attacks first encountered after the 85%
boundary. The split boundaries prevent overlapping windows from crossing
partitions, and the withheld category is excluded from model training, but
these results should not be presented as a pure future-only holdout without
revising and rerunning the experiment.

## Result provenance and utilities

- `results/results_final_leakfree/VERIFIED_RESULTS.md` identifies the
  historical pipeline and reports the headline values. Its claims are
  preserved as historical project-reported results, not independently
  validated by this cleanup.
- `src/generate_csv.py` writes tables from values hard-coded in the script; it
  does not calculate metrics or parse `run_final_eval.py` output.
- `src/run_benchmarks.py` separately trains an OC-SVM from training windows,
  loads the LSTM saved by evaluation, and times inference on windows from the
  final 15% only. Its latency population is not the same as the pooled attack
  evaluation population.
- `src/generate_diagnostic_histogram.py` requires the CSV and a saved OC-SVM
  model.
- The archived `src/get_chi2.py` recomputes paired statistics using attack
  windows from only the final 15% period, unlike the pooled withheld-attack
  population used by `run_final_eval.py`; it is not the source for the
  historical reported significance values.
- The existing `generate_figs.py` hard-codes deployment latency values that
  conflict with the later benchmark report, and synthesizes its plotted QBER
  traces. Those plots are not included in this clean snapshot.
- The older `run_experiments_v2.py` through `run_experiments_v5.py` and
  `figures_v2` through `figures_v5` are not the final evaluation workflow.
  In particular, v5 uses random score draws and a synthetic secondary dataset
  for reported-looking comparison plots; those outputs are not evidence of
  trained-model performance.
- The existing statistical-test provenance points to task logs not present in
  the folder. Statistical significance claims were not reproduced here.

## BB84 simulation

`src/run_qkd_simulation.py` uses NumPy random bits and bases to model idealized
BB84 sifting and an intercept-and-resend Eve. It compares sifted bits and
reports mean QBER and the fraction of trials below 10%. It does not model
physical noise or hardware, authentication, finite-key security, error
correction, privacy amplification, or production key derivation. A simulated
QBER response does not establish complete security, and the code does not
encrypt medical payloads.

The historical `VERIFIED_RESULTS.md` reports approximately 76.05% key
agreement when Eve is present. That value is not consistent with the current
function: its second return value is the fraction of trials whose QBER is
below 10%, rather than the bitwise agreement fraction of sifted keys. In one
cleanup run, the Eve-present case had 25.16% QBER and 0.00% of trials below
threshold. The discrepancy is preserved here rather than silently changing
the archived report.
