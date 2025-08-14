import jpype.imports
from jpype.types import JArray, JDouble
import numpy as np
from scipy.io import loadmat
from itertools import combinations
import os
import json
from common_scripts.common import jvm_setup, load_data
import configparser

# Load config
config = configparser.ConfigParser()
config.read('config.ini')

file_path = config['data']['file_path']
subject_number = config['data']['subject_index']

# ---- Set up ----
jvm_setup()
mat, ts_subject = load_data(file_path, subject_number)

# ---- Prepare Calculators ----
OInfoCalc = jpype.JClass("infodynamics.measures.continuous.gaussian.OInfoCalculatorGaussian")
SInfoCalc = jpype.JClass("infodynamics.measures.continuous.gaussian.SInfoCalculatorGaussian")

# ---- Compute O-Info and S-Info for all 3-node combinations ----
Nnodes = int(mat["Nnodes"][0][0])
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
output_path = f"results/metrics/subject_{subject_number}_triplets.json"
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
