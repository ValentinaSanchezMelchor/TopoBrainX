# run_oinfo_all_subjects.py

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

# ----- O-Information -----
OInfoCalc = jpype.JClass("infodynamics.measures.continuous.gaussian.OInfoCalculatorGaussian")

oinfo_all = []

for subj in range(Nsubjects):
    start = subj * Ntimepoints
    end = (subj + 1) * Ntimepoints
    ts_subject = ts[start:end, :]  # shape (200, 5)

    oinfo = OInfoCalc()
    oinfo.initialise(Nnodes)
    oinfo.setObservations(JArray(JDouble, 2)(ts_subject.tolist()))

    val = oinfo.computeAverageLocalOfObservations()
    oinfo_all.append(val)
    print(f"[{subj+1:02d}/{Nsubjects}] O-Information: {val:.6f}")

# Optional: Save to CSV or print stats
oinfo_all = np.array(oinfo_all)
print("\n--- Summary ---")
print(f"Mean: {oinfo_all.mean():.6f}")
print(f"Std:  {oinfo_all.std():.6f}")

jpype.shutdownJVM()
