#!/usr/bin/env python3

from collections import defaultdict
from ec.utils import write_dict, write_markers, read_markers


def setup_ec_index_args(parser):
    # index subparser
    index_info = "Index markers.txt file into groups, targets, and ec matrix files"
    parser_index = parser.add_parser(
        "index", description=index_info, help=index_info, add_help=True
    )

    # index subparser arguments
    parser_index.add_argument(
        "-g",
        "--groups",
        default=None,
        type=str,
        required=True,
        help="Path to output groups file",
    )
    parser_index.add_argument(
        "-t",
        "--targets",
        default=None,
        type=str,
        required=True,
        help="Path to output targets file",
    )
    parser_index.add_argument(
        "-e",
        "--ec",
        default=None,
        type=str,
        required=True,
        help="Path to output ec matrix",
    )
    parser_index.add_argument(
        "markers", metavar="markers.txt", type=str, help="Path to markers.txt file"
    )
    return parser_index


def validate_ec_index_args(parser, args):
    run_ec_index(args.groups, args.targets, args.ec, args.markers)


def run_ec_index(
    out_groups_fn, out_targets_fn, out_markers_ec_fn, markers_fname
):  # noqa
    markers_ec = defaultdict(list)
    celltypes = defaultdict()
    targets = defaultdict()
    read_markers(markers_fname, markers_ec, celltypes, targets)

    write_markers(out_markers_ec_fn, markers_ec)
    write_dict(out_groups_fn, celltypes)
    write_dict(out_targets_fn, targets)
