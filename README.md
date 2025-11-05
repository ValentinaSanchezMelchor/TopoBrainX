## TopoBrainX
This repository will include the to experiment to transform fMRI (or any timeseries data) into a combinatorial complex. These are the initial experiments and figures (no recent updates). The final code will be updated and made public once the the paper 'The Human Brain as a Combinatorial Complex' is published.

## Project Structure

```text
TopoBrainX/
│
├── data/
│   ├── NetSim/                  ← NetSim simulation .mat files
│   └── processed/               ← Kalman/AR filtered or preprocessed time series
│
├── notebooks/
│   └── explore_netsim.ipynb     ← Visualization of time series + ground-truth net
│
├── scripts/
│   ├── run_jidt_metrics.py      ← Runs O-info & S-info computation using JIDT
│   └── visualize_results.py     ← Plots for info measures and comparisons
│
├── results/
│   ├── figures/                 ← Visualizations of connectivity, synergy, etc.
│   └── metrics/                 ← Computed info-theoretic metrics per subject
│
├── src/
│   ├── info_theory/
│   │   ├── jidt_interface/          ← JPype setup + JIDT wrapper functions
│   │   ├── oinfo_sinfo_computation/ ← Core logic for O-info/S-info computation
│   │   └── tests/                   ← Unit tests for metrics
│   │
│   ├── preprocessing/
│   │   ├── kalman_filter.py        ← (Optional) Temporal filtering
│   │   └── zscore_normalize.py     ← Normalization routines
│   │
│   ├── complex_builder/            ← (Later) Construction of combinatorial complex
│   └── subset_selection/           ← (Skipped for now) Similarity hashing etc.
│
├── utils/
│   └── loader.py               ← NetSim data loader (load_ts_and_net)
│
├── requirements.txt           ← Include scipy, numpy, matplotlib, jpype1, etc.
├── README.md                  ← Project overview + usage
└── .gitignore                 ← Ignore processed data, checkpoints, etc.
```
---
## Description

**TopoBrainX** is a research codebase to:
- Extract relevant higher-order interactions from fMRI timeseries (NetSim/HCP).
- Apply Kalman filtering and similarity-based pruning.
- Construct combinatorial complex representations.
- Compute O-information / S-information.
- Visualize and interpret toy examples for the *"Human Brain as a Combinatorial Complex"* paper.
