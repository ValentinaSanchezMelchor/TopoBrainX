# scripts/construct_cc_subject.py

import os
import json
from scipy.io import loadmat
import numpy as np
from src.complex_builder.construct_cc import construct_cc

# ---- Settings ----
subject_idx = 0
sim_path = "data/NetSim/sims/sim1.mat"
triplet_metrics_path = f"results/metrics/subject_{subject_idx}_triplets.json"
output_path = f"results/metrics/subject_{subject_idx}_cc.json"

# ---- Load Data ----
print("[INFO] Loading NetSim .mat file...")
mat = loadmat(sim_path)
ts = mat["ts"]
Nsubjects = int(mat["Nsubjects"][0][0])
Ntimepoints = int(mat["Ntimepoints"][0][0])
Nnodes = int(mat["Nnodes"][0][0])

start = subject_idx * Ntimepoints
end = (subject_idx + 1) * Ntimepoints
ts_subject = ts[start:end, :]

# ---- Load Metrics ----
print(f"[INFO] Loading triplet metrics from: {triplet_metrics_path}")
with open(triplet_metrics_path, "r") as f:
    raw = json.load(f)
    # Convert string keys like "(1, 3, 4)" to tuples
    triplet_metrics = {
        tuple(map(int, k.strip("()").split(", "))): v
        for k, v in raw.items()
    }

# ---- Inspect Distribution (Auto Summary) ----

all_sinfo = np.array([v["sinfo"] for v in triplet_metrics.values()])
all_oinfo = np.array([v["oinfo"] for v in triplet_metrics.values()])

print("[INFO] --- Triplet Metric Summary ---")
print(f"S-Info: min={all_sinfo.min():.4f}, max={all_sinfo.max():.4f}, mean={all_sinfo.mean():.4f}, median={np.median(all_sinfo):.4f}")
print(f"O-Info: min={all_oinfo.min():.4f}, max={all_oinfo.max():.4f}, mean={all_oinfo.mean():.4f}, median={np.median(all_oinfo):.4f}")
print("[INFO] --------------------------------")

# Optional: Show top 3 highest synergy triplets
top_synergy = sorted(triplet_metrics.items(), key=lambda x: x[1]["sinfo"], reverse=True)[:3]
print("[INFO] Top 3 synergistic triplets:")
for t, v in top_synergy:
    print(f"  Triplet {t}: S-Info = {v['sinfo']:.4f}, O-Info = {v['oinfo']:.4f}")

# ---- Construct CC ----
print("[INFO] Constructing combinatorial complex...")
cc = construct_cc(
    ts_subject,
    triplet_metrics,
    edge_method="mi",
    edge_thresh=0.05,       # or higher if you want fewer edges
    sinfo_thresh=0.2,       # keep only strongly synergistic triplets
    oinfo_thresh=-0.002     # optional: use if you also want to filter based on O-Info
)

# ---- Save to JSON ----
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w") as f:
    json.dump(cc, f, indent=2)
print(f"[INFO] Saved CC to: {output_path}")