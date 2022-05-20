#!/usr/bin/env python3

from collections import defaultdict

def write_dict(fname, d):
    inv_d = {v: k for k, v in d.items()}
    with open(fname, "w") as f:
        for idx in range(len(d)):
            f.write(f"{inv_d[idx]}\n")
            
            
def write_markers(fname, markers):
    with open(fname, "w") as f:
        for k, v in markers.items():
            f.write(f"{k}\t")
            n = len(v)
            for idx, i in enumerate(v):
                f.write(f"{i}")
                if idx < n - 1:
                    f.write(",")
            f.write("\n")


def read_markers(
    fname,
    markers_ec: defaultdict(list),
    celltype: defaultdict(),
    marker_genes: defaultdict()
):
    with open(fname, "r") as f:
        for idx, line in enumerate(f.readlines()):
            ct, genes = line.strip().split("\t")
            celltype[ct] = idx

            # two things
            # 1. make marker_genes list
            # 2. make markers_ec
            for g in genes.split(","):
                gidx = len(marker_genes)

                # check if the gene has been added already
                if g in marker_genes.keys():  # gene repeated
                    gidx = marker_genes[g]
                else:
                    marker_genes[g] = gidx

                # for the cell type index, add the marker gene index
                markers_ec[celltype[ct]].append(marker_genes[g])

            # sort the marker genes
            markers_ec[celltype[ct]] = sorted(markers_ec[celltype[ct]])

def dict_to_list(groups, targets):
    groups = list(groups.keys())
    targets = list(targets.keys())
    return groups, targets

def read_ec_matrix(fname, markers_ec=defaultdict(list)):
    with open(fname, "r") as f:
        for idx, line in enumerate(f.readlines()):
            ct_id, gene_ids = line.strip().split("\t")
            markers_ec[int(ct_id)] = [int(i) for i in gene_ids.split(",")]
        
def read_markers_txt(fname, markers=defaultdict(list)):
    with open(fname, "r") as f:
        for idx, line in enumerate(f.readlines()):
            ct_id, gene_ids = line.strip().split("\t")
            markers[ct_id] = [i for i in gene_ids.split(",")]
                            
def read_txt(fname):
  with open (fname, 'r') as f:
    return [line.rstrip() for line in f]

