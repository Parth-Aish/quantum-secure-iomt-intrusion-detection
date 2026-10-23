# Quantum-Secured IoMT Intrusion Detection

This repository packages research code for exploring intrusion detection in
Internet of Medical Things (IoMT) and Wireless Body Area Network (WBAN)
telemetry. The repository name is an organizational name, not a confirmed
publication title.

## Research question

Can anomaly detection recognize attack categories withheld from supervised
training on WUSTL-EHMS-2020 traffic, and what does a small BB84 simulation show
about quantum bit error rate (QBER) under an intercept-and-resend model?

The project has two distinct components:

1. **Gateway anomaly detection:** a chronological, 30-row windowing pipeline
   compares supervised XGBoost/LightGBM baselines, Isolation Forest,
   autoencoders, and One-Class SVM.
2. **Communication-layer illustration:** a NumPy simulation of BB84 basis
   selection and intercept-and-resend. It is not a QKD implementation suitable
   for deployment, does not establish a secure key, and does not implement
   authentication, error correction, privacy amplification, a physical
   quantum channel, or AES encryption.

Federated learning, topology-aware attention, and a production security
gateway are not implemented by the final evaluation pipeline.

## Status and results

The values below are **previously reported project results**, transcribed from
[`VERIFIED_RESULTS.md`](results/results_final_leakfree/VERIFIED_RESULTS.md)
and its two CSV tables. They were **not regenerated during repository
preparation**. The source evaluation code was inspected, but its full training
run was not repeated because it is computationally expensive and writes model
artifacts.

| Withheld attack category | Model | Detection | FPR | F1 |
|---|---|---:|---:|---:|
| Spoofing (Experiment A) | One-Class SVM | 72.54% | 4.37% | 82.56% |
| Spoofing (Experiment A) | LSTM autoencoder | 73.94% | 13.03% | 80.60% |
| Data alteration (Experiment B) | One-Class SVM | 100.00% | 4.37% | 98.19% |
| Data alteration (Experiment B) | LSTM autoencoder | 100.00% | 13.03% | 94.78% |

The historic results document reports approximately 0% QBER without Eve and
approximately 24% with intercept-and-resend, using a 10% illustrative abort
threshold. One independent CLI run during cleanup returned 0.00% QBER and
100.00% accepted trials without Eve, and 25.16% QBER and 0.00% accepted trials
with Eve. This is the code's threshold-acceptance rate, not bitwise key
agreement. The historic document's 76.05% eavesdropper-case “key agreement”
does not match the current function's return definition and is not reproduced.
These are simulation outputs, not a security proof.

See [methodology](docs/methodology.md) for code-level qualifications and
[reproduction instructions](docs/reproduction.md) for exact commands and
important constraints.

## Data

The original folder contained a 3.95 MB CSV named
`wustl-ehms-2020_with_attacks_categories.csv`. It has 45 columns, including
source/destination address and MAC fields. It is not included here: its
provenance, redistribution rights, and handling of identifier-like fields
could not be established from the local materials.

The evaluation expects that exact filename and an annotated schema. Read
[`data/README.md`](data/README.md) before obtaining or using a dataset.

## Repository map

```text
src/                                Evaluation and support scripts
demo/app.py                         Optional Streamlit demonstration
data/README.md                      Dataset access and handling notes
results/results_final_leakfree/     Previously reported result summaries
docs/methodology.md                 Implementation and validity notes
docs/reproduction.md                Setup and command sequence
docs/data_dictionary.md             Expected CSV fields and preprocessing
tests/test_qkd.py                   Lightweight BB84 simulation checks
REPOSITORY_AUDIT.md                 File-by-file audit of the original folder
PUBLISHING_CHECKLIST.md             Decisions required before publication
```

## Environment and installation

The local environment observed during preparation was Python 3.13.14. Direct
dependencies and versions are recorded in [`requirements.txt`](requirements.txt)
from the installed environment; they are a starting point, not proof that
every end-to-end training run is reproducible on every platform.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Linux/macOS:

```sh
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

TensorFlow and the supervised/autoencoder baselines can require substantial
RAM and CPU/GPU time. Runtime and hardware requirements were not benchmarked
as part of this cleanup.

## Reproduction overview

1. Obtain the exact annotated input described in [`data/README.md`](data/README.md).
2. Run the final evaluation from `src` so the scripts' relative paths resolve:

   ```powershell
   Set-Location .\src
   python .\run_final_eval.py
   ```

   The script reads `..\data\wustl-ehms-2020_with_attacks_categories.csv` and
   writes model artifacts and a completion marker under
   `..\results\results_final_leakfree\`. It prints metrics to stdout; it does
   not itself write the existing `final_results.log` or generate the checked-in
   result CSVs.

3. After a successful evaluation, run inference benchmarks from the same
   directory:

   ```powershell
   python .\run_benchmarks.py
   ```

   This retrains the One-Class SVM, loads the LSTM artifact, and writes
   benchmark output and a plot. Do not treat it as a read-only command.
4. For code that merely formats the existing reported tables, see the warning
   in [reproduction.md](docs/reproduction.md); that helper uses hard-coded
   values rather than parsing an evaluation run.

The BB84 simulation can be run independently from the repository root:

```powershell
python .\src\run_qkd_simulation.py
```

## Optional demo

The demo needs the local CSV plus `lstm_model.h5` and
`ocsvm_model.joblib` in `results/results_final_leakfree/`. These model files
are intentionally not included because the underlying dataset's rights and
privacy implications are unresolved.

```powershell
streamlit run .\demo\app.py
```

The interface is illustrative, assumes precomputed models, and includes
displayed latency/memory figures; it is not a deployment benchmark or a
clinical/security product.

## Limitations and threats to validity

- The preprocessing and evaluation caveats in
  [`docs/methodology.md`](docs/methodology.md) limit the “leak-free” and
  future-generalization claims.
- The reported metrics have not been reproduced in this staged repository.
- The custom annotated CSV's creation process, official acquisition URL, and
  license are unknown.
- Existing statistical significance records point to a log not present in the
  project folder; do not cite them as independently verified here.
- No cryptographic key generation or payload encryption is implemented by the
  BB84 simulation.
- The dataset is a research benchmark and does not establish clinical safety,
  generalization to real patients, or operational suitability.

## Citation, license, and intended use

No verified publication citation, DOI, publication status, or project license
was found in the local materials. No `CITATION.cff` or `LICENSE` is supplied;
these require author confirmation. Dataset licensing is separate and remains
unresolved. See [`PUBLISHING_CHECKLIST.md`](PUBLISHING_CHECKLIST.md).

This repository supports academic research and is **not** a certified medical
device, clinical decision-support system, or production security system.
