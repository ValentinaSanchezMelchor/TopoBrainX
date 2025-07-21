import jpype
import jpype.imports
from jpype.types import JArray, JDouble
import numpy as np
import os

# Avoid numpy threading issues with JPype
os.environ['OMP_NUM_THREADS'] = '1'

# Path to JIDT jar file
jidt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "jidt_interface", "infodynamics.jar"))

# Start JVM
if not jpype.isJVMStarted():
    jpype.startJVM(jpype.getDefaultJVMPath(),
                   "-Djava.class.path=" + jidt_path,
                   "--enable-native-access=ALL-UNNAMED")

# Use Gaussian Mutual Info calculator
mi_class = jpype.JClass("infodynamics.measures.continuous.gaussian.MutualInfoCalculatorMultiVariateGaussian")
mi_calc = mi_class()

# Create 10 observations of 2D vectors
x = np.random.rand(10, 2)
y = x + 0.1 * np.random.rand(10, 2)  # correlated with noise

# Initialise with: vector_dim_x = 2, vector_dim_y = 2
mi_calc.initialise(2, 2)

# Set observations: must be (num_observations, vector_dim)
mi_calc.setObservations(JArray(JDouble, 2)(x.tolist()), JArray(JDouble, 2)(y.tolist()))

# Compute MI
mi = mi_calc.computeAverageLocalOfObservations()
print("Mutual Information:", mi)

jpype.shutdownJVM()