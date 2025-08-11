# run_oinfo_sinfo_triplets_subject.py

import jpype
import jpype.imports
from jpype.types import JArray, JDouble
import numpy as np
from scipy.io import loadmat
from itertools import combinations
import os
import json

# ---- JVM SETUP ----
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
subject_idx = 0  # You can change this to another subject index [0, ..., 49]
start = subject_idx * Ntimepoints
end = (subject_idx + 1) * Ntimepoints
ts_subject = ts[start:end, :]  # shape (200, 5)
print(f"[INFO] Subject {subject_idx+1} time series shape: {ts_subject.shape}")

# ---- Prepare Calculators ----
OInfoCalc = jpype.JClass("infodynamics.measures.continuous.gaussian.OInfoCalculatorGaussian")
SInfoCalc = jpype.JClass("infodynamics.measures.continuous.gaussian.SInfoCalculatorGaussian")

# ---- Compute O-Info and S-Info for all 3-node combinations ----
triplet_results = {}

triplets = list(combinations(range(Nnodes), 3))  # all 3-node subsets of [0,1,2,3,4]

for triplet in triplets:
    data = ts_subject[:, list(triplet)]  # shape (200, 3)

    # O-Info
    oinfo = OInfoCalc()
    oinfo.initialise(3)
    oinfo.setObservations(JArray(JDouble, 2)(data.tolist()))
    o_val = oinfo.computeAverageLocalOfObservations()

    # S-Info
    sinfo = SInfoCalc()
    sinfo.initialise(3)
    sinfo.setObservations(JArray(JDouble, 2)(data.tolist()))
    s_val = sinfo.computeAverageLocalOfObservations()

    triplet_results[triplet] = {"oinfo": o_val, "sinfo": s_val}
    print(f"Triplet {triplet}: O-Info = {o_val:.6f}, S-Info = {s_val:.6f}")


# ---- Save to JSON ----
output_path = f"results/metrics/subject_{subject_idx}_triplets.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Convert tuple keys to strings so json.dump() works
serializable_results = {
    str(k): v for k, v in triplet_results.items()
}

with open(output_path, "w") as f:
    json.dump(serializable_results, f, indent=2)

print(f"[INFO] Triplet results saved to {output_path}")


# ---- Done ----
jpype.shutdownJVM()