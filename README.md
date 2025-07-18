# TopoBrainX
This repository will include the to experiment to transform fMRI (or any timeseries data) into a combinatorial complex.

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
