import os
import numpy as np
import scipy.io

def load_netsim_data(data_dir):
    """
    Load all NetSim simulation files from the given directory.

    Args:
        data_dir (str): Path to the folder containing sim1.mat to sim28.mat

    Returns:
        ts_all: List of np.arrays (shape [Nsubjects, Ntimepoints, Nnodes])
        net_all: List of np.arrays (shape [Nsubjects, Nnodes, Nnodes])
    """
    ts_all = []
    net_all = []

    for i in range(1, 29):
        filename = f"sim{i}.mat"
        path = os.path.join(data_dir, filename)

        print(f"Loading {filename}...")
        data = scipy.io.loadmat(path)
        ts = data["ts"]     # shape: (Nsubjects * Ntimepoints, Nnodes)
        net = data["net"]   # shape: (Nsubjects, Nnodes, Nnodes)

        Nsubjects = net.shape[0]
        Nnodes = ts.shape[1]
        Ntimepoints = ts.shape[0] // Nsubjects

        ts_reshaped = ts.reshape(Nsubjects, Ntimepoints, Nnodes)

        ts_all.append(ts_reshaped)
        net_all.append(net)

    print("All 28 simulations loaded.")
    return ts_all, net_all