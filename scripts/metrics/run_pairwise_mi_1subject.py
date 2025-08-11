# scripts/metrics/run_pairwise_mi_1subject.py

import jpype
import jpype.imports
from jpype.types import JArray, JDouble
import numpy as np
from scipy.io import loadmat
import os
import json
from itertools import combinations

# ---- JVM Setup ----
os.environ['OMP_NUM_THREADS'] = '1'
jidt_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "src", "info_theory", "jidt_interface", "infodynamics.jar")
)
if not jpype.isJVMStarted():
    jpype.startJVM(classpath=[jidt_path])

# ---- Load Data ----
mat = loadmat("data/NetSim/sims/sim1.mat")
ts = mat["ts"]
Nsubjects = int(mat["Nsubjects"][0][0])
Ntimepoints = int(mat["Ntimepoints"][0][0])
Nnodes = int(mat["Nnodes"][0][0])

print(f"[INFO] ts shape: {ts.shape}")
print(f"[INFO] Nsubjects: {Nsubjects}, Ntimepoints: {Ntimepoints}, Nnodes: {Nnodes}")

# ---- Choose One Subject ----
subject_idx = 0  # You can change this
start = subject_idx * Ntimepoints
end = (subject_idx + 1) * Ntimepoints
ts_subject = ts[start:end, :]  # shape (200, Nnodes)
print(f"[INFO] Subject {subject_idx+1} time series shape: {ts_subject.shape}")

# ---- MI Calculator ----
MICalc = jpype.JClass("infodynamics.measures.continuous.gaussian.MutualInfoCalculatorMultiVariateGaussian")

pairwise_mi = {}

for i, j in combinations(range(Nnodes), 2):
    calc = MICalc()
    calc.initialise(1, 1)  # Each signal is 1D
    calc.setObservations(
        JArray(JDouble, 2)(ts_subject[:, [i]].tolist()),
        JArray(JDouble, 2)(ts_subject[:, [j]].tolist())
    )
    mi_val = calc.computeAverageLocalOfObservations()
    pairwise_mi[f"{i},{j}"] = mi_val
    print(f"Pair ({i}, {j}): MI = {mi_val:.6f}")

# ---- Save Results ----
output_path = f"results/metrics/subject_{subject_idx}_pairwise.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w') as f:
    json.dump(pairwise_mi, f, indent=2)

print(f"[INFO] Saved pairwise MI to {output_path}")

jpype.shutdownJVM()