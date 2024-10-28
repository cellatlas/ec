#!/usr/bin/env python3

import pandas as pd
from ec.utils import write_markers


def setup_ec_mark_args(parser):
    mark_info = "Created markers.txt from deg.txt file"
    parser_mark = parser.add_parser(
        "mark", description=mark_info, help=mark_info, add_help=True
    )

    # mark subparser arguments
    parser_mark.add_argument(
        "-p",
        "--mp",
        default=None,
        type=float,
        required=True,
        help="Minimum corrected p-value",
    )
    parser_mark.add_argument(
        "-f",
        "--mfc",
        default=None,
        type=float,
        required=True,
        help="Minimum log2 fold-change",
    )
    parser_mark.add_argument(
        "-g",
        "--gs",
        default=None,
        type=int,
        required=True,
        help="Maximum number of genes shared",
    )
    parser_mark.add_argument(
        "-m",
        "--mpct",
        default=None,
        type=int,
        required=True,
        help="Maximum number of genes per cell type",
    )
    parser_mark.add_argument(
        "-o",
        "--output",
        default=None,
        type=str,
        required=True,
        help="Output path",
    )
    parser_mark.add_argument(
        "degs",
        metavar="degs.txt",
        type=str,
        help="Path to degs.txt file to extract markers from",
    )
    parser_mark.add_argument(
        "-fmt",
        "--format",
        default="txt",
        type=str,
        required=False,
        help="Output format",
        choices=["txt", "json"],
    )

    return parser_mark


def validate_ec_mark_args(parser, args):
    markers = run_ec_mark(args.mp, args.mfc, args.gs, args.mpct, args.output, args.degs)

    if args.format == "json":
        import json

        json_data = markers.to_dict(orient="records")
        with open(args.output, "w") as f:
            json.dump(json_data, f, indent=4)
    else:
        # make dictionary
        markers_dict = (
            markers.groupby("group")["target"].apply(lambda x: list(x)).to_dict()
        )
        write_markers(args.output, markers_dict)

    return


def run_ec_mark(mp, mfc, gs, mpct, output_fname, deg_fname):

    # read dataframe
    df = pd.read_csv(deg_fname, sep="\t")

    markers = ec_mark(df, mp, mfc, gs, mpct)

    return markers


def ec_mark(df, min_pval, min_logfc, max_gene_share, max_per_celltype):
    # column names
    pval_col_name = "p_corr"
    fc_col_name = "log_fc"
    rank_col_name = "rank"
    # filter by criteria
    dfc = df.query(f"{pval_col_name} <= {min_pval} & {fc_col_name} >= {min_logfc}")

    # mask out genes that are shared between max_gene_shares cell type
    non_repeat_genes = (
        dfc["target"]
        .value_counts()[dfc["target"].value_counts() < max_gene_share]
        .index.values
    )

    # remove repeated genes, sort by effect size

    m = dfc[dfc.target.isin(non_repeat_genes)].sort_values(
        rank_col_name, ascending=True
    )

    # get number of genes per cell type to extract
    n_sample = min(m["group"].value_counts().min(), max_per_celltype)

    # extract markers with highet effect size
    markers = m.groupby("group").tail(n_sample)
    return markers

    #   {
    #     "cell_type": "human ASPCs",
    #     "cell_state": "None",
    #     "gene": "PDGFRA",
    #     "source": {
    #       "source_id": "text",
    #       "source_type": "text",
    #       "source_rationale": "We identified six distinct subpopulations of human ASPCs (see Supplementary Note 1) in subclustered scRNA-seq and sNuc-seq samples, all of which express the common marker gene PDGFRA (Extended Data Fig. 7a, b)."
    #     }
    #   },
