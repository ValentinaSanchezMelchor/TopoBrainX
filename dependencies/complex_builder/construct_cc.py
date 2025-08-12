# dependencies/complex_builder/construct_cc.py

import json
import os
from itertools import combinations
import numpy as np
import sklearn

def load_triplet_metrics(filepath):
    with open(filepath, "r") as f:
        raw = json.load(f)
    # Convert string keys back to tuples
    triplet_metrics = {
        tuple(map(int, k.strip("()").split(", "))): v
        for k, v in raw.items()
    }
    return triplet_metrics

def compute_pairwise_mi(ts_subject):
    """
    Compute pairwise mutual information matrix (symmetric).
    """
    from sklearn.feature_selection import mutual_info_regression
    N = ts_subject.shape[1]
    mi_matrix = np.zeros((N, N))
    for i, j in combinations(range(N), 2):
        mi = mutual_info_regression(ts_subject[:, [i]], ts_subject[:, j], discrete_features=False)[0]
        mi_matrix[i, j] = mi_matrix[j, i] = mi
    return mi_matrix

def construct_cc(ts_subject, triplet_metrics, edge_method="mi", edge_thresh=0.05, oinfo_thresh=0.001, sinfo_thresh=0.1):
    """
    Construct a combinatorial complex with:
    - edges based on MI or other pairwise metric
    - triangles based on oinfo/sinfo thresholds
    """
    N = ts_subject.shape[1]
    nodes = list(range(N))
    edges = set()
    triangles = set()

    # Edges
    if edge_method == "mi":
        mi_matrix = compute_pairwise_mi(ts_subject)
        for i, j in combinations(nodes, 2):
            if mi_matrix[i, j] >= edge_thresh:
                edges.add((i, j))

    # Triangles (2-simplices) — you can tune oinfo and sinfo thresholds as needed
    for triplet, metrics in triplet_metrics.items():
        if (
            metrics.get("sinfo", 0) >= sinfo_thresh
            and metrics.get("oinfo", 0) >= oinfo_thresh
        ):
            triangles.add(tuple(sorted(triplet)))

    return {
        "nodes": nodes,
        "edges": sorted(list(edges)),
        "triplets": [list(t) for t in sorted(triangles)]
    }