import os
import jpype
import sys

from numpy.testing.print_coercion_tables import print_new_cast_table
from scipy.io import loadmat
import configparser

def jvm_setup():
    # ---- JVM SETUP ----
    os.environ['OMP_NUM_THREADS'] = '1'
    jidt_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__),"..", "..", "dependencies", "info_theory", "jidt_interface", "infodynamics.jar")
    )
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=[jidt_path])

def load_data(file_path, subject_index): # Choose one subject

    # ---- Load Data ----
    mat = loadmat(file_path)
    ts = mat["ts"]
    Nsubjects = int(mat["Nsubjects"][0][0])
    Ntimepoints = int(mat["Ntimepoints"][0][0])
    Nnodes = int(mat["Nnodes"][0][0])

    print(f"[INFO] ts shape: {ts.shape}")
    print(f"[INFO] Nsubjects: {Nsubjects}, Ntimepoints: {Ntimepoints}, Nnodes: {Nnodes}")

    # ---- Choose One Subject ----
    subject_idx = int(subject_index)  # You can change this to another subject index [0, ..., 49]
    start = subject_idx * Ntimepoints
    end = (subject_idx + 1) * Ntimepoints
    ts_subject = ts[start:end, :]  # shape (200, 5)
    print(f"[INFO] Subject {subject_idx+1} time series shape: {ts_subject.shape}")

    return mat, ts_subject