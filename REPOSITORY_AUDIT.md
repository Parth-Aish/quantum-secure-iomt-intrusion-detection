# Repository audit

## Scope and safety

The source folder was inspected recursively, including hidden entries, file
sizes, source references, and the directory structure. Before staging, it
contained **177 files totaling 176,062,443 bytes** (about 168 MiB), with no
hidden files and no `.git` directory. The original files were not moved,
deleted, or edited. The clean snapshot is in the sibling
`Downloads\quantum-secure-iomt-intrusion-detection` staging directory next
to the untouched `Papers` source folder.

No Git history, remotes, or commit metadata were available because the source
folder is not a Git repository. Therefore historical secret exposure cannot
be assessed.

## Findings

- **Main evaluation entry point:** `src/run_final_eval.py`. It sorts by
  `Packet_num`, fits scaling on normal rows in the first 70%, and constructs
  non-boundary-crossing 30-row windows. It trains supervised baselines,
  unsupervised detectors, and autoencoders. It writes model artifacts and a
  completion marker; it prints results but does not generate the checked-in
  result tables.
- **Supporting entry points:** `src/run_benchmarks.py` loads the LSTM,
  independently fits an OC-SVM, and writes benchmark outputs; `src/
  run_qkd_simulation.py` is an independent NumPy simulation. The demo depends
  on local models and the excluded CSV.
- **Scientific validity:** the full-data one-hot encoding occurs before the
  split. In addition, attack windows from the first 85% are appended to
  evaluation collections, so the withheld-category metrics are not a
  strictly future-only test. These details are recorded in
  [`docs/methodology.md`](docs/methodology.md).
- **Results:** the nested `results/results_final_leakfree/VERIFIED_RESULTS.md`
  and tables are preserved in staging as historically reported results.
  They were not reproduced during this cleanup. The duplicate root-level
  `results_final_leakfree/` has divergent Markdown/log files; matching CSVs
  and model artifacts are byte-identical, but the folders are not identical.
- **QKD result discrepancy:** one CLI simulation run during cleanup returned
  25.16% QBER and 0.00% accepted trials with Eve. The historic verified-results
  document's 76.05% “key agreement” conflicts with the function's return
  definition (fraction of trials below the 10% threshold); the discrepancy is
  documented and not silently corrected.
- **Non-reproducible presentations:** `src/generate_csv.py` exports literal
  metrics; it does not compute them. `generate_figs.py` hard-codes deployment
  values that conflict with reported benchmarks and creates synthetic QBER
  lines. `run_experiments_v5.py` draws random scores and a synthetic secondary
  dataset. Those visual artifacts are not included.
- **Dataset:** 3,946,888 bytes and 45 columns. The header contains
  `SrcAddr`, `DstAddr`, `SrcMac`, and `DstMac`. No official source URL,
  redistribution license, or provenance for the `_with_attacks_categories`
  annotation was present locally. The dataset is excluded pending legal and
  privacy review.
- **Dependencies:** there were no dependency manifests. The current machine
  has Python 3.13.14 and the exact versions in the staging `requirements.txt`;
  Qiskit is not installed and is not imported by the final BB84 simulation.
- **Sensitive-information scan:** no credential/token/password pattern was
  identified in scanned text files. The source contains author/supervisor
  names in internal evaluation documents, published-author contact details in
  `references_dump.txt`, a placeholder email in the manuscript, and an
  absolute local path in `notebook_code.py`. These materials are not copied
  into the public snapshot. This was a pattern scan, not a guarantee that
  sensitive information is absent.
- **Copyright/confidentiality:** literature PDFs, manuscript variants,
  internal presentations/reports, and submission bundles are excluded or
  marked for human review; no redistribution permission was established.
- **Publication metadata:** no verified project license, paper citation, DOI,
  or publication status was found. The staging snapshot intentionally omits
  `LICENSE` and `CITATION.cff`.

## Classification definitions

- **KEEP** — core public-snapshot file, small result record, or source needed
  for a documented workflow; included in staging.
- **OPTIONAL** — useful helper/demo but not required for the main evaluation;
  included only when its behavior is documented.
- **ARCHIVE** — historical/experimental or superseded material; preserve in
  the original folder but do not include in the main snapshot.
- **EXCLUDE** — generated, duplicate, environment-specific, third-party, or
  potentially sensitive item not suitable for the public snapshot.
- **INVESTIGATE** — publication, rights, privacy, provenance, or claim review
  is needed before any public distribution.

The inventory below classifies every file found in the original folder.

| Original path | Size (bytes) | Class | Reason |
|---|---:|---|---|
| `archive\check_stats.py` | 4850 | ARCHIVE | Superseded experiments/checkpoints/results; original preserved, not part of final workflow. |
| `archive\generate_outputs.py` | 9201 | ARCHIVE | Superseded experiments/checkpoints/results; original preserved, not part of final workflow. |
| `archive\results_strengthened\all_results.json` | 8992 | ARCHIVE | Superseded experiments/checkpoints/results; original preserved, not part of final workflow. |
| `archive\results_strengthened\dense_ae_seed42.keras` | 158387 | ARCHIVE | Superseded experiments/checkpoints/results; original preserved, not part of final workflow. |
| `archive\results_strengthened\fig_pr_roc_curves.pdf` | 20297 | ARCHIVE | Superseded experiments/checkpoints/results; original preserved, not part of final workflow. |
| `archive\results_strengthened\fig_pr_roc_curves.png` | 169722 | ARCHIVE | Superseded experiments/checkpoints/results; original preserved, not part of final workflow. |
| `archive\results_strengthened\gru_ae_seed42.keras` | 261293 | ARCHIVE | Superseded experiments/checkpoints/results; original preserved, not part of final workflow. |
| `archive\results_strengthened\loss_curve.png` | 35077 | ARCHIVE | Superseded experiments/checkpoints/results; original preserved, not part of final workflow. |
| `archive\results_strengthened\lstm_ae_seed123.keras` | 317782 | ARCHIVE | Superseded experiments/checkpoints/results; original preserved, not part of final workflow. |
| `archive\results_strengthened\lstm_ae_seed2024.keras` | 317786 | ARCHIVE | Superseded experiments/checkpoints/results; original preserved, not part of final workflow. |
| `archive\results_strengthened\lstm_ae_seed314.keras` | 317786 | ARCHIVE | Superseded experiments/checkpoints/results; original preserved, not part of final workflow. |
| `archive\results_strengthened\lstm_ae_seed42.keras` | 317778 | ARCHIVE | Superseded experiments/checkpoints/results; original preserved, not part of final workflow. |
| `archive\results_strengthened\lstm_ae_seed7.keras` | 317778 | ARCHIVE | Superseded experiments/checkpoints/results; original preserved, not part of final workflow. |
| `archive\results_strengthened\mcnemar_results.csv` | 421 | ARCHIVE | Superseded experiments/checkpoints/results; original preserved, not part of final workflow. |
| `archive\results_strengthened\table3_supervised_baselines.csv` | 840 | ARCHIVE | Superseded experiments/checkpoints/results; original preserved, not part of final workflow. |
| `archive\results_strengthened\table4_zero_day.csv` | 1357 | ARCHIVE | Superseded experiments/checkpoints/results; original preserved, not part of final workflow. |
| `archive\results_strengthened\table6_deployment.csv` | 202 | ARCHIVE | Superseded experiments/checkpoints/results; original preserved, not part of final workflow. |
| `archive\run_experiments.py` | 42180 | ARCHIVE | Superseded experiments/checkpoints/results; original preserved, not part of final workflow. |
| `archive\run_proper_training.py` | 6473 | ARCHIVE | Superseded experiments/checkpoints/results; original preserved, not part of final workflow. |
| `archive\run_strengthening.py` | 8064 | ARCHIVE | Superseded experiments/checkpoints/results; original preserved, not part of final workflow. |
| `archive\Untitled8.ipynb` | 442857 | ARCHIVE | Superseded experiments/checkpoints/results; original preserved, not part of final workflow. |
| `citations_output.txt` | 16508 | EXCLUDE | Reference dump/generated output includes contact details or unverified extracted material. |
| `clean_paper.py` | 1433 | ARCHIVE | Legacy document manipulation helper; can overwrite/recreate source artifacts and is not needed for evaluation. |
| `convert_md_tex.py` | 7154 | ARCHIVE | Legacy document manipulation helper; can overwrite/recreate source artifacts and is not needed for evaluation. |
| `data\wustl-ehms-2020_with_attacks_categories.csv` | 3946888 | INVESTIGATE | Dataset source/license and annotation provenance unknown; includes address/MAC-style fields; not copied. |
| `demo\app.py` | 10707 | OPTIONAL | Optional helper/demo; copied into staging with limitations documented. |
| `docs\figures\fig1_class_distribution.pdf` | 17776 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\fig1_class_distribution.png` | 103728 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\fig10_architecture.pdf` | 18692 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\fig10_architecture.png` | 142021 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\fig11_bb84_simulation.pdf` | 21879 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\fig11_bb84_simulation.png` | 147798 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\fig2_feature_importance.pdf` | 21725 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\fig2_feature_importance.png` | 190515 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\fig3_confusion_matrices.pdf` | 18516 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\fig3_confusion_matrices.png` | 91269 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\fig4_roc_curves.pdf` | 21537 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\fig4_roc_curves.png` | 184163 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\fig5_baseline_comparison.pdf` | 20096 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\fig5_baseline_comparison.png` | 98813 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\fig6_threshold_optimization.pdf` | 22554 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\fig6_threshold_optimization.png` | 197213 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\fig7_zero_day_detection.pdf` | 22187 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\fig7_zero_day_detection.png` | 136026 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\fig8_reconstruction_error.pdf` | 20673 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\fig8_reconstruction_error.png` | 98199 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\fig9_correlation_heatmap.pdf` | 27537 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\fig9_correlation_heatmap.png` | 144194 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\table_baselines.csv` | 859 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\table_thresholds.csv` | 6152 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures\table_zero_day.csv` | 1176 | ARCHIVE | Earlier generated figures/tables with unverified provenance; not needed for final workflow. |
| `docs\figures_leakfree\fig1_baseline_comparison.png` | 148003 | EXCLUDE | Generated plots based on hard-coded/outdated values or synthetic QBER trace; not scientifically traceable. |
| `docs\figures_leakfree\fig2_deployment.png` | 68321 | EXCLUDE | Generated plots based on hard-coded/outdated values or synthetic QBER trace; not scientifically traceable. |
| `docs\figures_leakfree\fig3_qber.png` | 192698 | EXCLUDE | Generated plots based on hard-coded/outdated values or synthetic QBER trace; not scientifically traceable. |
| `docs\figures_leakfree\fig4_pr_roc_curves.png` | 135513 | EXCLUDE | Generated plots based on hard-coded/outdated values or synthetic QBER trace; not scientifically traceable. |
| `docs\outputs\Elsevier_Submission_Bundle.zip` | 44835 | INVESTIGATE | Submission bundle may contain unpublished or third-party material; contents/rights require review. |
| `docs\outputs\fig1_baseline_comparison.pdf` | 17917 | EXCLUDE | Generated plots based on hard-coded/outdated values or synthetic QBER trace; not scientifically traceable. |
| `docs\outputs\fig2_deployment.pdf` | 15581 | EXCLUDE | Generated plots based on hard-coded/outdated values or synthetic QBER trace; not scientifically traceable. |
| `docs\outputs\fig3_qber.pdf` | 19042 | EXCLUDE | Generated plots based on hard-coded/outdated values or synthetic QBER trace; not scientifically traceable. |
| `docs\outputs\Phase_II_Evaluation.pdf` | 40717 | INVESTIGATE | Generated manuscript/internal report includes unverified claims and/or identifying information; review before sharing. |
| `docs\outputs\Phase_II_Evaluation.tex` | 10799 | INVESTIGATE | Generated manuscript/internal report includes unverified claims and/or identifying information; review before sharing. |
| `docs\outputs\Procedia_Manuscript.pdf` | 73009 | INVESTIGATE | Generated manuscript/internal report includes unverified claims and/or identifying information; review before sharing. |
| `docs\outputs\Procedia_Manuscript.tex` | 20483 | INVESTIGATE | Generated manuscript/internal report includes unverified claims and/or identifying information; review before sharing. |
| `docs\outputs\Results_and_Outcomes_Report.pdf` | 332088 | INVESTIGATE | Generated manuscript/internal report includes unverified claims and/or identifying information; review before sharing. |
| `docs\outputs\Results_and_Outcomes_Report.tex` | 9914 | INVESTIGATE | Generated manuscript/internal report includes unverified claims and/or identifying information; review before sharing. |
| `docs\Phase_1_Presentation.md` | 3039 | INVESTIGATE | Internal or manuscript material with author/supervisor details and claims inconsistent with final code. |
| `docs\Phase_1_Presentation.pptx` | 34029 | INVESTIGATE | Internal or manuscript material with author/supervisor details and claims inconsistent with final code. |
| `docs\Phase_1_Synopsis.md` | 3860 | INVESTIGATE | Internal or manuscript material with author/supervisor details and claims inconsistent with final code. |
| `docs\Phase_II_Evaluation.md` | 8886 | INVESTIGATE | Internal or manuscript material with author/supervisor details and claims inconsistent with final code. |
| `docs\Revised_Manuscript.md` | 19066 | INVESTIGATE | Internal or manuscript material with author/supervisor details and claims inconsistent with final code. |
| `extract_refs.py` | 487 | ARCHIVE | Legacy document manipulation helper; can overwrite/recreate source artifacts and is not needed for evaluation. |
| `figures_v2\fig1_tda_normal.pdf` | 20265 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v2\fig1_tda_normal.png` | 159385 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v2\fig2_tda_spoofing.pdf` | 21094 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v2\fig2_tda_spoofing.png` | 163985 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v2\fig3_attention_maps.pdf` | 47786 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v2\fig3_attention_maps.png` | 107561 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v2\fig4_federated_convergence.pdf` | 21970 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v2\fig4_federated_convergence.png` | 287528 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v2\fig5_zero_day_comparison.pdf` | 22095 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v2\fig5_zero_day_comparison.png` | 132482 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v2\fig6_quantum_security.pdf` | 24226 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v2\fig6_quantum_security.png` | 191833 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v3\fig1_ablation_study.pdf` | 26501 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v3\fig1_ablation_study.png` | 110170 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v3\fig2_federated_convergence.pdf` | 19972 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v3\fig2_federated_convergence.png` | 219243 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v4\fig_ablation.pdf` | 25859 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v4\fig_ablation.png` | 110154 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v4\fig_evasion.pdf` | 19149 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v4\fig_evasion.png` | 115640 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v4\fig_overhead.pdf` | 18710 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v4\fig_overhead.png` | 106240 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v4\fig_qkd_limits.pdf` | 22712 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v4\fig_qkd_limits.png` | 180849 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v4\fig_sensitivity.pdf` | 23263 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v4\fig_sensitivity.png` | 146998 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v5\fig_ablation.pdf` | 26232 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v5\fig_ablation.png` | 110709 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v5\fig_evasion.pdf` | 20227 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v5\fig_evasion.png` | 170204 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v5\fig_overhead.pdf` | 20413 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v5\fig_overhead.png` | 147248 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v5\fig_sensitivity.pdf` | 27304 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `figures_v5\fig_sensitivity.png` | 149450 | ARCHIVE | Historical or exploratory figures; source/results not part of final reproducible pipeline. |
| `fix_paths.py` | 3609 | ARCHIVE | Legacy document manipulation helper; can overwrite/recreate source artifacts and is not needed for evaluation. |
| `generate_figs.py` | 2230 | EXCLUDE | Hard-coded/outdated performance values and synthetic QBER plot; outputs are not reproducible evidence. |
| `Manuscript.pdf` | 142939 | INVESTIGATE | Manuscript/submission material has unresolved authorship/publication rights or conflicts with final implementation. |
| `Manuscript.tex` | 12062 | INVESTIGATE | Manuscript/submission material has unresolved authorship/publication rights or conflicts with final implementation. |
| `Matrix\Literature_Matrix.xlsx` | 43509 | ARCHIVE | Research planning/literature matrix, not required to run final evaluation; inspect rights before sharing. |
| `Matrix\Matrix.py` | 10952 | ARCHIVE | Research planning/literature matrix, not required to run final evaluation; inspect rights before sharing. |
| `notebook_code.py` | 194952 | EXCLUDE | Notebook-export/install snippet with local absolute path and non-reproducible setup. |
| `Paper.pdf` | 1070846 | INVESTIGATE | Manuscript/submission material has unresolved authorship/publication rights or conflicts with final implementation. |
| `Phase_1_Synopsis.pdf` | 4444 | INVESTIGATE | Manuscript/submission material has unresolved authorship/publication rights or conflicts with final implementation. |
| `Read\A_Quantum_Generative_Adversarial_Network-based_Intrusion_Detection_System.pdf` | 1274948 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\A_Secure_Ensemble_Learning-Based_Fog-Cloud_Approach_for_Cyberattack_Detection_in_IoMT.pdf` | 1440368 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\A_Signature-Based_Wireless_Intrusion_Detection_System_Framework_for_Multi-Channel_Man-in-the-Middle_Attacks_Against_Protected_Wi-Fi_Networks.pdf` | 3402954 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\Deep_Learning-Based_Intrusion_Detection_System_for_Detecting_IoT_Botnet_Attacks_A_Review.pdf` | 3452843 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\Dew-Cloud-Based_Hierarchical_Federated_Learning_for_Intrusion_Detection_in_IoMT.pdf` | 1974708 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\Edge-Federated_Learning-Based_Intelligent_Intrusion_Detection_System_for_Heterogeneous_Internet_of_Things.pdf` | 5603212 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\Empowering_Healthcare_With_IoMT_Evolution_Machine_Learning_Integration_Security_and_Interoperability_Challenges.pdf` | 6597827 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\Enhanced_Multigrained_Scanning-Based_Deep_Stacking_Network_for_Intrusion_Detection_in_IoMT_Networks.pdf` | 2564029 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\Enhancing_Malicious_Activity_Detection_in_IoT-Enabled_Network_and_IoMT_Systems_Through_Meta-Heuristic_Optimization_and_Machine_Learning.pdf` | 8505755 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\Explainable_AI_based_Improved_Intrusion_Detection_System_in_Wireless_Sensor_Networks.pdf` | 551040 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\Explainable_Artificial_Intelligence_XAI_for_Internet_of_Things_A_Survey.pdf` | 3927503 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\Federated_Learning_for_IoMT_Applications_A_Standardization_and_Benchmarking_Framework_of_Intrusion_Detection_Systems.pdf` | 3243960 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\Federated_Quantum-Based_Privacy-Preserving_Threat_Detection_Model_for_Consumer_Internet_of_Things.pdf` | 1086199 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\Healthcare_Internet_of_Things_Security_Threats_Challenges_and_Future_Research_Directions.pdf` | 5391664 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\Intrusion_Detection_System_for_Wireless_Sensor_Networks_A_Machine_Learning_Based_Approach.pdf` | 2662237 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\Intrusion_Detection_Systems_Using_Quantum-Inspired_Density_Matrix_Encodings.pdf` | 530573 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\IoMT-TrafficData_Dataset_and_Tools_for_Benchmarking_Intrusion_Detection_in_Internet_of_Medical_Things.pdf` | 2890093 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\Machine_Learning_for_Healthcare-IoT_Security_A_Review_and_Risk_Mitigation.pdf` | 6392538 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\Meta-IDS_Meta-Learning-Based_Smart_Intrusion_Detection_System_for_Internet_of_Medical_Things_IoMT_Network.pdf` | 2710051 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\Network_Anomaly_Detection_Using_Quantum_Neural_Networks_on_Noisy_Quantum_Computers.pdf` | 1668082 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\Network_Intrusion_Detection_An_IoT_and_Non_IoT-Related_Survey.pdf` | 4649684 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\Network_Intrusion_Detection_Method_Based_on_CNN-BiLSTM-Attention_Model.pdf` | 1103725 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\Privacy-Preserving_Federated_Learning_for_Intrusion_Detection_in_IoT_Environments_A_Survey.pdf` | 3984953 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\Quantum-Resistant_Wireless_Intrusion_Detection_System_using_Machine_Learning_Techniques.pdf` | 395304 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\SmartSentry_Cyber_Threat_Intelligence_in_Industrial_IoT.pdf` | 5012018 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `Read\Stochastic_Gradient_Descent_Intrusions_Detection_for_Wireless_Sensor_Network_Attack_Detection_System_Using_Machine_Learning.pdf` | 1709129 | EXCLUDE | Third-party research paper PDF; redistribution rights not established. |
| `references_dump.txt` | 16182 | EXCLUDE | Reference dump/generated output includes contact details or unverified extracted material. |
| `results\results_final_leakfree\benchmarks.txt` | 112 | KEEP | Core reproducibility script or preserved final result summary; copied into staging. |
| `results\results_final_leakfree\completed.txt` | 19 | EXCLUDE | Generated log/marker/diagnostic image; redundant or not a primary reproducibility artifact. |
| `results\results_final_leakfree\final_results.log` | 16246 | EXCLUDE | Generated log/marker/diagnostic image; redundant or not a primary reproducibility artifact. |
| `results\results_final_leakfree\lstm_model.h5` | 318900 | INVESTIGATE | Trained model may encode source examples; dataset rights and model privacy risk unresolved; not copied. |
| `results\results_final_leakfree\ocsvm_model.joblib` | 4949871 | INVESTIGATE | Trained model may encode source examples; dataset rights and model privacy risk unresolved; not copied. |
| `results\results_final_leakfree\ocsvm_spoofing_histogram.png` | 109184 | EXCLUDE | Generated log/marker/diagnostic image; redundant or not a primary reproducibility artifact. |
| `results\results_final_leakfree\table_zero_day_expA.csv` | 270 | KEEP | Core reproducibility script or preserved final result summary; copied into staging. |
| `results\results_final_leakfree\table_zero_day_expB.csv` | 276 | KEEP | Core reproducibility script or preserved final result summary; copied into staging. |
| `results\results_final_leakfree\VERIFIED_RESULTS.md` | 3902 | KEEP | Core reproducibility script or preserved final result summary; copied into staging. |
| `results_final_leakfree\completed.txt` | 19 | EXCLUDE | Duplicate root-level results folder; copied equivalent summaries from canonical nested results where appropriate. |
| `results_final_leakfree\final_results.log` | 22058 | EXCLUDE | Duplicate root-level results folder; copied equivalent summaries from canonical nested results where appropriate. |
| `results_final_leakfree\lstm_model.h5` | 318900 | EXCLUDE | Duplicate root-level results folder; copied equivalent summaries from canonical nested results where appropriate. |
| `results_final_leakfree\ocsvm_model.joblib` | 4949871 | EXCLUDE | Duplicate root-level results folder; copied equivalent summaries from canonical nested results where appropriate. |
| `results_final_leakfree\table_zero_day_expA.csv` | 270 | EXCLUDE | Duplicate root-level results folder; copied equivalent summaries from canonical nested results where appropriate. |
| `results_final_leakfree\table_zero_day_expB.csv` | 276 | EXCLUDE | Duplicate root-level results folder; copied equivalent summaries from canonical nested results where appropriate. |
| `results_final_leakfree\VERIFIED_RESULTS.md` | 3874 | EXCLUDE | Duplicate root-level results folder; copied equivalent summaries from canonical nested results where appropriate. |
| `Revised_Manuscript_Clean.md` | 19066 | INVESTIGATE | Manuscript/submission material has unresolved authorship/publication rights or conflicts with final implementation. |
| `run_experiments_v2.py` | 17406 | ARCHIVE | Superseded exploratory experiment; not the final evaluation entry point. |
| `run_experiments_v3.py` | 9047 | ARCHIVE | Superseded exploratory experiment; not the final evaluation entry point. |
| `run_experiments_v4.py` | 12109 | ARCHIVE | Superseded exploratory experiment; not the final evaluation entry point. |
| `run_experiments_v5.py` | 12029 | ARCHIVE | Superseded exploratory experiment; not the final evaluation entry point. |
| `src\__pycache__\run_qkd_simulation.cpython-313.pyc` | 2762 | EXCLUDE | Compiled Python cache; generated and interpreter-specific. |
| `src\gather_stats.py` | 492 | OPTIONAL | Optional helper/demo; copied into staging with limitations documented. |
| `src\generate_csv.py` | 1291 | OPTIONAL | Optional helper/demo; copied into staging with limitations documented. |
| `src\generate_diagnostic_histogram.py` | 3475 | OPTIONAL | Optional helper/demo; copied into staging with limitations documented. |
| `src\generate_eval_tex.py` | 11022 | ARCHIVE | Auxiliary report/statistics script; depends on prior model outputs or creates internal reports, not core workflow. |
| `src\generate_report_tex.py` | 10854 | ARCHIVE | Auxiliary report/statistics script; depends on prior model outputs or creates internal reports, not core workflow. |
| `src\run_final_eval.py` | 12114 | KEEP | Core reproducibility script or preserved final result summary; copied into staging. |
| `src\run_qkd_simulation.py` | 2027 | KEEP | Core reproducibility script or preserved final result summary; copied into staging. |
| `tectonic.zip` | 18959851 | EXCLUDE | Bundled executable/tool archive is environment-specific and not project source. |
| `tectonic\tectonic.exe` | 49320448 | EXCLUDE | Bundled executable/tool archive is environment-specific and not project source. |
| `verify_citations.py` | 1912 | ARCHIVE | Manuscript-specific citation validation utility; requires unpublished manuscript context. |
| `verify_strict.py` | 1891 | ARCHIVE | Manuscript-specific citation validation utility; requires unpublished manuscript context. |
| `archive\results_strengthened\multi_seed_robustness.json` | 1372 | ARCHIVE | Superseded experiment output; preserve in the original archive, not part of the final workflow. |
| `src\get_chi2.py` | 3883 | ARCHIVE | Auxiliary significance script uses a different final-period test population; not part of the reported final workflow. |
| `src\run_benchmarks.py` | 5367 | KEEP | Core benchmark script; copied into staging with its output behavior documented. |
