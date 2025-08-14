import jpype
import jpype.imports
from jpype.types import JArray, JDouble
import numpy as np
from scipy.io import loadmat
import os

# ----- JVM Setup -----
os.environ['OMP_NUM_THREADS'] = '1'
jidt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "infodynamics.jar"))
if not jpype.isJVMStarted():
    jpype.startJVM(classpath=[jidt_path])

# ----- Load One Subject from netsim -----
mat = loadmat("data/netsim/sims/sim1.mat")
ts = mat["ts"]            # shape: (10000, 5)
ts_subject = ts[0:200, :] # one subject: shape (200, 5)

print("[INFO] Loaded subject shape:", ts_subject.shape)

# ----- O-Information -----
OInfoCalc = jpype.JClass("infodynamics.measures.continuous.gaussian.OInfoCalculatorGaussian")
oinfo = OInfoCalc()
oinfo.initialise(ts_subject.shape[1])  # num variables
oinfo.setObservations(JArray(JDouble, 2)(ts_subject.tolist()))

value = oinfo.computeAverageLocalOfObservations()
print("O-Information:", value)

jpype.shutdownJVM()