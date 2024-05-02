#!/usr/bin/env python3

from collections import defaultdict
from ec.utils import read_markers_txt, write_markers


def setup_ec_check_args(parser):
    # filter subparser
    check_info = "check markers.txt file"
    parser_check = parser.add_parser(
        "check", description=check_info, help=check_info, add_help=True
    )

    parser_check.add_argument(
        "-o",
        "--output",
        default=None,
        type=str,
        required=False,
        help="Path to output checked markers.txt file",
    )
    parser_check.add_argument(
        "markers", metavar="markers.txt", type=str, help="Path to markers.txt file"
    )
    return parser_check


def validate_ec_check_args(parser, args):
    run_ec_check(args.output, args.markers)


def run_ec_check(output, markers_fname):

    markers = defaultdict(list)
    header = []
    read_markers_txt(markers_fname, markers, header)

    is_antichain(markers)


def is_antichain(sets):
    # Check each pair of sets in the input
    groups = list(sets.keys())
    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            # If one set is a subset of the other, print which ones and return False
            s1 = set(sets[groups[i]])
            s2 = set(sets[groups[j]])
            if s1.issubset(s2) or s2.issubset(s1):
                print(
                    f"Group {groups[i]}: {s1} and \nGroup {groups[j]}: {s2} are comparable."
                )

                return False
    # If no sets are subsets of others, it's an antichain
    return True
