## TopoBrainX
This repository will include the to experiment to transform fMRI (or any timeseries data) into a combinatorial complex. These are the initial experiments and figures (no recent updates). The code here is the one used to construct the figures on the extented abstract accepted at the NeurReps Workshop 2025. The final code will be updated and made public once the the paper 'The Human Brain as a Combinatorial Complex' is published. The NetSim data is publicly available and can be accessed here: https://www.fmrib.ox.ac.uk/datasets/netsim/index.html.

## Project Structure

```text
TopoBrainX/
│
├── data/
│   ├── NetSim/                  ← NetSim simulation .mat files
│   └── processed/               ← Kalman/AR filtered or preprocessed time series (not included yet)
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
│   │   ├── kalman_filter.py        ← Temporal filtering (not included yet)
│   │   └── zscore_normalize.py     ← Normalization routines (not included yet)
│   │
│   ├── complex_builder/            ← Construction of combinatorial complex
│   └── subset_selection/           ← (Skipped for now) Similarity hashing etc.
│
├── utils/
│   └── loader.py               ← NetSim data loader 
│
├── requirements.txt           ← Include scipy, numpy, matplotlib, jpype1, etc.
├── README.md                  ← Project overview + usage
└── .gitignore                 ← Ignore processed data, checkpoints, etc.
```
---
## Description

**TopoBrainX** is a research codebase to:
- Extract relevant higher-order interactions from fMRI timeseries (NetSim).
- Construct combinatorial complex representations.
- Compute O-information / S-information.
- Visualize and interpret toy examples for the *"Human Brain as a Combinatorial Complex"* paper. The code here is the one used to construct the figures on the extented abstract accepted at the NeurReps Workshop 2025.
