#!/usr/bin/env python3

from collections import defaultdict
from ec.utils import read_markers_txt, write_markers, read_txt
import pandas as pd


def setup_ec_convert_args(parser):
    # filter subparser
    convert_info = "Convert file from marker gene names to ids given a t2g file"
    parser_convert = parser.add_parser(
        "convert", description=convert_info, help=convert_info, add_help=True
    )

    # convert subparser arguments
    parser_convert.add_argument(
        "-m",
        "--mapfile",
        default=None,
        type=str,
        required=True,
        help="Path to mapping file",
    )
    parser_convert.add_argument(
        "-o",
        "--output",
        default=None,
        type=str,
        required=True,
        help="Path to output converted markers.txt file",
    )
    parser_convert.add_argument(
        "-b",
        "--bad_targets",
        default=None,
        type=str,
        required=False,
        help="Path to targets that are not converted",
    )

    parser_convert.add_argument(
        "markers", metavar="markers.txt", type=str, help="Path to markers.txt file"
    )
    return parser_convert


def validate_ec_convert_args(parser, args):
    run_ec_convert(args.mapfile, args.output, args.markers, args.bad_targets)


def run_ec_convert(map_fn, output, markers_fname, bad_targets_fname):

    markers = defaultdict(list)
    header = []
    read_markers_txt(markers_fname, markers, header)

    df = pd.read_csv(map_fn, sep="\t", header=None, names=["name0", "name1"])
    df["name1"].fillna(df["name0"], inplace=True)

    # map the gene symbol in the marker list for each celltype from name0 to name1,
    # note that df is a pandas dataframe and may not have unique mapping from name0 to name1
    # in which case, add all duplicates to the marker list
    converted_markers = defaultdict(list)
    counter = 0
    bad = []
    for ct in markers.keys():
        for idx, target in enumerate(markers[ct]):
            if target in df["name0"].values:
                idxs = df[df["name0"] == target].index
                for i in idxs:
                    converted_markers[ct].append(df["name1"][i])
            else:
                # keep the original gene symbol if not found in mapping file
                bad.append(target)
                converted_markers[ct].append(target)
                print(f"{target} not found in mapping file")
                counter += 1

    print(f"Number of mapped elements not found in mapping file: {counter}")

    write_markers(output, converted_markers, header)

    if bad:
        with open(bad_targets_fname, "w") as f:
            for item in bad:
                f.write("%s\n" % item)
    else:
        # Create an empty file if bad is empty
        open(bad_targets_fname, "w").close()
