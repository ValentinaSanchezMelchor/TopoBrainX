import jpype
import jpype.imports
from jpype.types import JArray, JDouble
import numpy as np
import os

os.environ['OMP_NUM_THREADS'] = '1'

jidt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "infodynamics.jar"))

if not jpype.isJVMStarted():
    jpype.startJVM(classpath=[jidt_path])

# Create O-information calculator
OInfoCalc = jpype.JClass("infodynamics.measures.continuous.gaussian.OInfoCalculatorGaussian")
oinfo = OInfoCalc()

# Dummy data: 5 observations, 3 variables
X = np.array([
    [1.0, 2.0, 3.0],
    [1.1, 2.1, 3.1],
    [0.9, 1.8, 3.2],
    [1.2, 2.2, 3.0],
    [0.8, 2.0, 3.3]
])

oinfo.initialise(X.shape[1])  # number of variables
oinfo.setObservations(JArray(JDouble, 2)(X.tolist()))
value = oinfo.computeAverageLocalOfObservations()
print("O-Information:", value)

jpype.shutdownJVM()