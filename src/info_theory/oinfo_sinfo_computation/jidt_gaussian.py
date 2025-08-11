# src/info_theory/oinfo_sinfo_computation/jidt_gaussian.py

import jpype
import jpype.imports
from jpype.types import JArray, JDouble
import numpy as np
import os

def start_jvm():
    """Ensure the JVM is started with the correct path."""
    jidt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "jidt_interface", "infodynamics.jar"))
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=[jidt_path])

def compute_oinfo(data: np.ndarray) -> float:
    """Compute O-information for a multivariate Gaussian system."""
    start_jvm()
    OInfoCalc = jpype.JClass("infodynamics.measures.continuous.gaussian.OInfoCalculatorGaussian")()
    OInfoCalc.initialise()
    OInfoCalc.setObservations(JArray(JDouble, 2)(data.tolist()))
    return OInfoCalc.computeAverageLocalOfObservations()

def compute_sinfo(data: np.ndarray) -> float:
    """Compute S-information for a multivariate Gaussian system."""
    start_jvm()
    SInfoCalc = jpype.JClass("infodynamics.measures.continuous.gaussian.SInfoCalculatorGaussian")()
    SInfoCalc.initialise()
    SInfoCalc.setObservations(JArray(JDouble, 2)(data.tolist()))
    return SInfoCalc.computeAverageLocalOfObservations()