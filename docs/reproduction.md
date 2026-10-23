# Reproduction guide

The commands below describe the current scripts. A complete reproduction
requires the exact annotated input CSV; its acquisition and redistribution
status are unresolved. Existing results are not guaranteed to reproduce
without matching data, software, and hardware.

## 1. Create an environment

Use Python 3.13.14, the interpreter observed during repository preparation,
then install the versions in `requirements.txt`.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Linux/macOS:

```sh
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

TensorFlow install availability depends on the platform and Python build. If
installation fails, use a supported Python/TensorFlow combination and record
the changed versions rather than silently substituting dependencies.

## 2. Obtain and check the input

Follow [`../data/README.md`](../data/README.md). Place an appropriately
licensed and reviewed file at:

```text
data/wustl-ehms-2020_with_attacks_categories.csv
```

The scripts expect all 45 fields listed in
[`data_dictionary.md`](data_dictionary.md), including `Packet_num`, `Label`,
and `Attack Category`. The repository does not include code to recreate the
annotated CSV from an official raw download.

## 3. Run the final evaluation

Run from the source directory because input/output paths are relative to the
current working directory:

```powershell
Set-Location .\src
python .\run_final_eval.py
```

```sh
cd src
python run_final_eval.py
```

This trains XGBoost, LightGBM, Isolation Forest, Dense/GRU/LSTM
autoencoders, and One-Class SVM. It writes LSTM and OC-SVM model files plus a
completion marker in `results/results_final_leakfree/` (relative to `src`).
Capture stdout separately if a run log is desired. It does not create the
existing result-table CSVs.

The full training suite was not run during this cleanup. It may be
computationally expensive; no run-time estimate is established.

## 4. Run benchmark and supporting scripts

After the evaluation has created model files, run from `src`:

```powershell
python .\run_benchmarks.py
python .\gather_stats.py
```

The benchmark script retrains and saves the OC-SVM, overwrites benchmark
output, and creates a plot under `src/figures_leakfree/`. The stats helper
loads the resulting model artifacts. These scripts are not read-only.

`generate_csv.py` writes the previously reported table values from literals in
the script. It is a formatting/export helper, **not** a metric reproduction
step. Do not use its successful completion as evidence that the metrics were
recomputed.

## 5. Run the independent simulation and tests

From the repository root:

```powershell
python .\src\run_qkd_simulation.py
python -m unittest discover -s tests -v
```

The QKD simulation is stochastic; its output will vary across runs. Tests
check the expected ideal/no-Eve and intercept-and-resend behavior, not real
quantum security.

## 6. Optional Streamlit demo

The demo additionally needs the CSV and the two locally generated model
artifacts at `results/results_final_leakfree/lstm_model.h5` and
`results/results_final_leakfree/ocsvm_model.joblib`.

```powershell
streamlit run .\demo\app.py
```

It displays sample windows and model inferences; its displayed latency and
memory values are static presentation values rather than live measurements.
