#!/usr/bin/env python3

from collections import defaultdict 
from ec.index import ec_index
from ec.utils import (write_dict, write_markers, read_markers, read_ec_matrix, read_txt, dict_to_list)

import numpy as np

def check_index_files(markers_ec, targets, groups):
  # Check for skipped indices in markers_ec
  if not list(markers_ec.keys()) == list(range(len(markers_ec.keys()))):
    print('ERROR: Invalid ec matrix file: one or more indices missing')
    return False

  # Check for duplicated marker genes in targets.txt
  elif not len(targets) == len(np.unique(targets)):
    print('ERROR: Invalid targets file: duplicated marker gene found')
    return False

  # Check for duplicated cell types in groups.txt
  elif not len(groups) == len(np.unique(groups)):
    print('ERROR: Invalid groups file: duplicated cell type found')
    return False
  else:
    return True

# Step 2: Check if the 3 index files are compatible within each other.

def check_compatibility_index_files(markers_ec, targets, groups):
  if not len(groups) == len(markers_ec.keys()):
    print("ERROR: groups and ec matrix files are not compatible: different number of cell types found")
    return False
  elif not len(targets) == len(set([j for sub in markers_ec.values() for j in sub])):
    print('ERROR: targets and ec matrix files are not compatible: different number of marker genes found')
  else:
    return True


def check_markers_to_index(markers_fn, groups, targets, markers_ec):
  check_markers_ec = defaultdict(list)
  check_groups = defaultdict(list)
  check_targets = defaultdict(list)
  read_markers(markers_fn, check_markers_ec, check_groups, check_targets)
  check_groups, check_targets = dict_to_list(check_groups, check_targets)
  if not groups == check_groups or not targets == check_targets or not markers_ec == check_markers_ec:
    print('ERROR: markers.txt is not compatible with provided ec matrix')
    return False

  else:
    return True



def ec_verify(groups_fn, targets_fn, markers_ec_fn, markers_fname):
    groups = read_txt(groups_fn)
    targets = read_txt(targets_fn)
    markers_ec = defaultdict(list)
    read_ec_matrix(markers_ec_fn, markers_ec)
    
    # First step: Check of individual files:
    if not check_index_files(markers_ec, targets, groups):
        return

    # Second step: Check if the 3 index files are compatible within each other
    elif not check_compatibility_index_files(markers_ec, targets, groups):
        return

    # Third step: See if indices files originates from provided markers
    elif not check_markers_to_index(markers_fname, groups, targets, markers_ec):
        return

    else:
        print("Files are correct")
