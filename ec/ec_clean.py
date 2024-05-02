#!/usr/bin/env python3

from collections import defaultdict
from ec.utils import read_markers_txt, write_markers


def setup_ec_clean_args(parser):
    # filter subparser
    clean_info = "clean markers.txt file"
    parser_clean = parser.add_parser(
        "clean", description=clean_info, help=clean_info, add_help=True
    )

    parser_clean.add_argument(
        "-o",
        "--output",
        default=None,
        type=str,
        required=True,
        help="Path to output cleaned markers.txt file",
    )
    parser_clean.add_argument(
        "markers", metavar="markers.txt", type=str, help="Path to markers.txt file"
    )
    return parser_clean


def validate_ec_clean_args(parser, args):
    run_ec_clean(args.output, args.markers)


def run_ec_clean(output, markers_fname):

    markers = defaultdict(list)
    read_markers_txt(markers_fname, markers)

    # combine duplicate cell types by 1. taking the union of the markers and 2. keep only the unique marker names
    cleaned_markers = defaultdict(list)
    for ct in markers.keys():
        cleaned_markers[ct] += list(set(markers[ct]))

    for ct in cleaned_markers.keys():
        cleaned_markers[ct] = list(set(cleaned_markers[ct]))

    write_markers(output, cleaned_markers)
