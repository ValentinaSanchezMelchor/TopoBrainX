## TopoBrainX
This repository will include the to experiment to transform fMRI (or any timeseries data) into a combinatorial complex.

## Project Structure

```text
TopoBrainX/
│
├── data/
│   ├── raw/               ← NetSim files go here
│   └── processed/         ← Kalman-filtered or preprocessed timeseries
│
├── notebooks/             ← Exploratory analysis and figures
├── scripts/               ← Individual experiment stages
├── results/
│   ├── figures/           ← Output visualizations
│   └── metrics/           ← O-info / S-info values, etc.
│
├── src/
│   ├── info_theory/       ← JIDT-based information metrics
│   ├── preprocessing/     ← Kalman filter, z-scoring, etc.
│   ├── subset_selection/  ← Similarity / hashing to prune candidate sets
│   └── complex_builder/   ← Combinatorial complex construction
│
├── utils/                 ← Helper functions (plotting, loading, etc.)
├── README.md              ← Project overview
└── .gitignore             ← Ignore checkpoints, processed data
```
---
## Description

**TopoBrainX** is a research codebase to:
- Extract relevant higher-order interactions from fMRI timeseries (NetSim/HCP).
- Apply Kalman filtering and similarity-based pruning.
- Construct combinatorial complex representations.
- Compute O-information / S-information.
- Visualize and interpret toy examples for the *"Human Brain as a Combinatorial Complex"* paper.
