# scripts/metrics/run_pairwise_mi_1subject.py
import sys

import jpype
import jpype.imports
from jpype.types import JArray, JDouble
import numpy as np
from scipy.io import loadmat
import os
import json
from itertools import combinations
from common_scripts.common import jvm_setup, load_data

# ---- Set up ----

subject_number = sys.argv[1]
jvm_setup()
mat, ts_subject = load_data(int(subject_number))


# ---- MI Calculator ----
Nnodes = int(mat["Nnodes"][0][0])
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
output_path = f"results/metrics/subject_{subject_number}_pairwise.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w') as f:
    json.dump(pairwise_mi, f, indent=2)

print(f"[INFO] Saved pairwise MI to {output_path}")

jpype.shutdownJVM()