#!/usr/bin/env python3

from collections import defaultdict 
from utils import (read_markers_txt, write_markers)

def ec_merge(marker_1_fname, marker_2_fname, o_fname, method):

  markers_1 = defaultdict(list)
  markers_2 = defaultdict(list)

  read_markers_txt(marker_1_fname, markers_1)
  read_markers_txt(marker_2_fname, markers_2)

  set_1 = set(markers_1.keys())
  set_2 = set(markers_2.keys())

  if method == 'intersect':
    common_keys = set_1.intersection(set_2)

    inters_markers = defaultdict(list)
    for key in common_keys:
      inters_markers[key] = list(set(markers_1[key]).intersection(set(markers_2[key])))

    write_markers(o_fname, inters_markers)
    
  elif method == 'union':
    union_keys = set_1.union(set_2)

    union_markers = defaultdict(list)
    for key in union_keys:
      union_markers[key] = list(set(markers_1[key]).union(set(markers_2[key])))

    write_markers(o_fname, union_markers)
