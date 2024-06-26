#!/usr/bin/env python3

from collections import defaultdict
from ec.utils import read_markers_txt, write_markers, read_txt


def setup_ec_filter_args(parser):
    # filter subparser
    filter_info = " Filter out bad genes from markers.txt file"
    parser_filter = parser.add_parser(
        "filter", description=filter_info, help=filter_info, add_help=True
    )

    # filter subparser arguments
    parser_filter.add_argument(
        "-bt",
        "--bad-targets",
        default=None,
        type=str,
        required=True,
        help="Path to bad targets file",
    )
    parser_filter.add_argument(
        "-o",
        "--output",
        default=None,
        type=str,
        required=True,
        help="Path to output filtered markers.txt file",
    )
    parser_filter.add_argument(
        "markers", metavar="markers.txt", type=str, help="Path to markers.txt file"
    )
    return parser_filter


def validate_ec_filter_args(parser, args):
    run_ec_filter(args.bad_targets, args.output, args.markers)


def run_ec_filter(bad_targets_fname, output, markers_fname):

    markers = defaultdict(list)
    header = []
    read_markers_txt(markers_fname, markers, header)

    bad_targets = read_txt(bad_targets_fname)

    for ct in markers.keys():
        for target in bad_targets:
            if target in markers[ct]:
                markers[ct].remove(target)

    write_markers(output, markers, header)
