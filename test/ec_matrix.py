from scipy.sparse import csr_matrix
from scipy.io import mmwrite
from collections import defaultdict
import numpy as np


def read_markers_ec(fname, markers_ec=defaultdict(list)):
    with open(fname, "r") as f:
        for idx, line in enumerate(f.readlines()):
            ct_id, gene_ids = line.strip().split("\t")
            markers_ec[int(ct_id)] = [int(i) for i in gene_ids.split(",")]


def ec_matrix(markers_ec_fn, out_matrix_fn):
    markers_ec = defaultdict(list)
    read_markers_ec(markers_ec_fn, markers_ec)
    n_clusters = len(list(markers_ec.keys()))
    n_features = np.unique(sum(list(markers_ec.values()), [])).shape[0]
    B = np.zeros((n_clusters, n_features))
    for k, v in markers_ec.items():
        B[k][v] = 1
    mtx = csr_matrix(B).astype(int)
    mmwrite(out_matrix_fn, mtx)
