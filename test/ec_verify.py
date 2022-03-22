#!/usr/bin/env python3

from scipy.sparse import csr_matrix
from scipy.io import mmwrite
from collections import defaultdict, Counter
import numpy as np
import sys
import os


def read_markers_ec(fname, markers_ec=defaultdict(list)):
    with open(fname, "r") as f:
        for idx, line in enumerate(f.readlines()):
            ct_id, gene_ids = line.strip().split("\t")
            markers_ec[int(ct_id)] = [int(i) for i in gene_ids.split(",")]

def read_txt(fname):
  with open (fname, 'r') as f:
    return [line.rstrip() for line in f]

def index_markers(
    markers_fname,
):
    celltype = defaultdict()
    marker_genes = defaultdict()
    markers_ec = defaultdict(list)
    groups = []
    elements = []
    with open(markers_fname, "r") as f:
        for idx, line in enumerate(f.readlines()):
            ct, genes = line.strip().split("\t")
            groups.append(ct)
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
                    elements.append(g)

                # for the cell type index, add the marker gene index
                markers_ec[celltype[ct]].append(marker_genes[g])

            # sort the marker genes
            markers_ec[celltype[ct]] = sorted(markers_ec[celltype[ct]])
            elements = sorted(elements)
        return markers_ec, groups, elements


# Step 1: Check if each of the 3 files is correct

def check_index_files(markers_ec, elements, groups):
  # Check for skipped indices in markers_ec
  if not list(markers_ec.keys()) == list(range(len(markers_ec.keys()))):
    print('ERROR: Invalid markers_ec file: one or more indices missing')
    return False

  # Check for duplicated marker genes in elements.txt
  elif not len(elements) == len(np.unique(elements)):
    print('ERROR: Invalid elements.txt file: duplicated marker gene found')
    return False

  # Check for duplicated cell types in groups.txt
  elif not len(groups) == len(np.unique(groups)):
    print('ERROR: Invalid groups.txt file: duplicated cell type found')
    return False
  else:
    return True

# Step 2: Check if the 3 index files are compatible within each other.

def check_compatibility_index_files(markers_ec, elements, groups):
  if not len(groups) == len(markers_ec.keys()):
    print("ERROR: groups.txt and markers.ec files are not compatible: different number of cell types found")
    return False
  elif not len(elements) == len(set([j for sub in markers_ec.values() for j in sub])):
    print('ERROR: elements.txt and markers.ec files are not compatible: different number of marker genes found')
  else:
    return True


def check_markers_to_index(markers_fn):
  check_ec, check_groups, check_elements = index_markers(markers_fn)

  if not groups == check_groups or not sorted(elements) == check_elements or not markers_ec == check_ec:
    print('ERROR: markers.txt is not compatible with markers_ec')
    return False

  else:
    return True



def ec_verify(markers_ec, elements, groups, markers_fname):
  # First step: Check of individual files:
  if not check_index_files(markers_ec, elements, groups):
    return

  # Second step: Check if the 3 index files are compatible within each other
  elif not check_compatibility_index_files(markers_ec, elements, groups):
    return
  
  # Third step: See if indices files originates from provided markers
  elif not check_markers_to_index(markers_fname):
    return

  else:
    print("Provided files are correct")
  

if __name__ == '__main__':
    markers_ec_fname = sys.argv[1]
    elements_fname = sys.argv[2]
    groups_fname = sys.argv[3]
    markers_fname = sys.argv[4]

    groups = read_txt(groups_fname)

    elements = read_txt(elements_fname)

    markers_ec = defaultdict(list)
    read_markers_ec(markers_ec_fname, markers_ec)

    ec_verify(markers_ec, elements, groups, markers_fname)   


