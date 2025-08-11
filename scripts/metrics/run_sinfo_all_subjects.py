# scripts/metrics/run_sinfo_all_subjects.py

import jpype
import jpype.imports
from jpype.types import JArray, JDouble
import numpy as np
from scipy.io import loadmat
import os

# ----- JVM Setup -----
os.environ['OMP_NUM_THREADS'] = '1'
jidt_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..", "..",  # go up from scripts/metrics
        "src", "info_theory", "jidt_interface", "infodynamics.jar"
    )
)
if not jpype.isJVMStarted():
    jpype.startJVM(classpath=[jidt_path])

# ----- Load NetSim Data -----
mat = loadmat("data/NetSim/sims/sim1.mat")
ts = mat["ts"]
Nsubjects = int(mat["Nsubjects"][0][0])
Ntimepoints = int(mat["Ntimepoints"][0][0])
Nnodes = int(mat["Nnodes"][0][0])

print(f"[INFO] ts shape: {ts.shape}")
print(f"[INFO] Nsubjects: {Nsubjects}, Ntimepoints: {Ntimepoints}, Nnodes: {Nnodes}")

# ----- S-Information -----
SInfoCalc = jpype.JClass("infodynamics.measures.continuous.gaussian.SInfoCalculatorGaussian")

sinfo_all = []

for subj in range(Nsubjects):
    start = subj * Ntimepoints
    end = (subj + 1) * Ntimepoints
    ts_subject = ts[start:end, :]  # shape (200, 5)

    sinfo = SInfoCalc()
    sinfo.initialise(Nnodes)
    sinfo.setObservations(JArray(JDouble, 2)(ts_subject.tolist()))

    val = sinfo.computeAverageLocalOfObservations()
    sinfo_all.append(val)
    print(f"[{subj+1:02d}/{Nsubjects}] S-Information: {val:.6f}")

# Optional: Save to CSV or print stats
sinfo_all = np.array(sinfo_all)
print("\n--- Summary ---")
print(f"Mean: {sinfo_all.mean():.6f}")
print(f"Std:  {sinfo_all.std():.6f}")

jpype.shutdownJVM()
