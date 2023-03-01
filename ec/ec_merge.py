#!/usr/bin/env python3

from collections import defaultdict
from ec.utils import read_markers_txt, write_markers


def setup_ec_merge_args(parser):
    # merge subparser
    merge_info = "Merge two markers.txt files (union or intersection)"
    parser_merge = parser.add_parser(
        "merge", description=merge_info, help=merge_info, add_help=True
    )

    # merge subparser arguments
    parser_merge.add_argument(
        "-o",
        "--output",
        default=None,
        type=str,
        required=True,
        help="Path to output merged markers.txt file",
    )
    parser_merge.add_argument(
        "-m",
        "--method",
        choices=["intersection", "union"],
        type=str,
        required=True,
        help="Method to merge. Intersection or union",
    )
    parser_merge.add_argument(
        "markers_1",
        metavar="markers.txt_1",
        type=str,
        help="Path to first markers.txt file",
    )
    parser_merge.add_argument(
        "markers_2",
        metavar="markers.txt_2",
        type=str,
        help="Path to second markers.txt file",
    )
    return parser_merge


def validate_ec_merge_args(parser, args):
    run_ec_merge(args.markers_1, args.markers_2, args.output, args.method)


def run_ec_merge(marker_1_fname, marker_2_fname, o_fname, method):

    markers_1 = defaultdict(list)
    markers_2 = defaultdict(list)

    read_markers_txt(marker_1_fname, markers_1)
    read_markers_txt(marker_2_fname, markers_2)

    if method == "intersect":
        m = ec_merge_intersect(markers_1, markers_2)

    elif method == "union":
        m = ec_merge_union(markers_1, markers_2)
    else:
        raise NotImplementedError()

    write_markers(o_fname, m)


def ec_merge_union(markers_1, markers_2):
    set_1 = set(markers_1.keys())
    set_2 = set(markers_2.keys())
    union_keys = set_1.union(set_2)

    union_markers = defaultdict(list)
    for key in union_keys:
        union_markers[key] = list(set(markers_1[key]).union(set(markers_2[key])))
    return union_markers


def ec_merge_intersect(markers_1, markers_2):
    set_1 = set(markers_1.keys())
    set_2 = set(markers_2.keys())
    common_keys = set_1.intersection(set_2)

    inters_markers = defaultdict(list)
    for key in common_keys:
        inters_markers[key] = list(
            set(markers_1[key]).intersection(set(markers_2[key]))
        )
    return inters_markers
