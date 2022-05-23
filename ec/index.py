#!/usr/bin/env python3

from collections import defaultdict 
from ec.utils import (write_dict, write_markers, read_markers)

def ec_index(
    out_groups_fn, out_targets_fn, out_markers_ec_fn, markers_fname
):  # noqa
    markers_ec = defaultdict(list)
    celltypes = defaultdict()
    targets = defaultdict()
    read_markers(markers_fname, markers_ec, celltypes, targets)

    write_markers(out_markers_ec_fn, markers_ec)
    write_dict(out_groups_fn, celltypes)
    write_dict(out_targets_fn, targets)
