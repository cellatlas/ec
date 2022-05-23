import argparse
import sys

from ec.index import ec_index
from ec.verify import ec_verify
from ec.merge import ec_merge
from ec.mark import ec_mark

def main():
    """
    Main ec function to use the package from the command line
    """

    # Define parent parser
    parser = argparse.ArgumentParser(
        description=f"ec", add_help=False
    )
    # Initiate subparsers
    subparsers = parser.add_subparsers(dest="command")
    # Define parent (not sure why I need both parent parser and parent, but otherwise it does not work)
    #parent = argparse.ArgumentParser(add_help=False)

    # Add custom help argument to parent parser
    parser.add_argument(
        "-h", "--help", action="store_true", help="Print help."
    )

    # index subparser
    index_info = "Index markers.txt file into groups, targets, and ec matrix files"
    parser_index = subparsers.add_parser(
        "index", description=index_info, help=index_info, add_help=True
    )

    # index subparser arguments
    parser_index.add_argument(
        "-g",
        "--groups",
        default=None,
        type=str,
        required = True,
        help="Path to output groups file",
    )
    parser_index.add_argument(
        "-t",
        "--targets",
        default=None,
        type=str,
        required = True,
        help="Path to output targets file",
    )
    parser_index.add_argument(
        "-e",
        "--ec",
        default=None,
        type=str,
        required = True,
        help="Path to output ec matrix",
    )
    parser_index.add_argument(
        'markers',
        metavar='markers.txt',
        type=str,
        help='Path to markers.txt file'
    )


    # verify subparser
    verify_info = "Check whether the provided groups, targets, ec matrix and markers.txt files are correct and compatible with each other"
    parser_verify = subparsers.add_parser(
        "verify", description=verify_info, help=verify_info, add_help=True
    )

    # verify subparser arguments
    parser_verify.add_argument(
        "-g",
        "--groups",
        default=None,
        type=str,
        required = True,
        help="Path to groups file to verify",
    )
    parser_verify.add_argument(
        "-t",
        "--targets",
        default=None,
        type=str,
        required = True,    
        help="Path to targets file to verify",
    )
    parser_verify.add_argument(
        "-e",
        "--ec",
        default=None,
        type=str,
        required = True,    
        help="Path to ec matrix to verify",
    )
    parser_verify.add_argument(
        'markers',
        metavar='markers.txt',
        type=str,
        help='Path to markers.txt file to verify'
    )


    # merge subparser
    merge_info = "Merge two markers.txt files (union or intersection)"
    parser_merge = subparsers.add_parser(
        "merge", description=merge_info, help=merge_info, add_help=True
    )

    # merge subparser arguments
    parser_merge.add_argument(
        "-o",
        "--output",
        default=None,
        type=str,
        required = True,    
        help="Path to output merged markers.txt file",
    )
    parser_merge.add_argument(
        "-m",
        "--method",
        choices=['intersection', 'union'],
        type=str,
        required = True,
        help='Method to merge. Intersection or union'
    )
    parser_merge.add_argument(
        "markers_1",
        metavar='markers.txt_1',
        type=str,
        help="Path to first markers.txt file",
    )
    parser_merge.add_argument(
        "markers_2",
        metavar='markers.txt_2',
        type=str,
        help="Path to second markers.txt file",
    )


    # mark subparser
    mark_info = "Created markers.txt from deg.txt file"
    parser_mark = subparsers.add_parser(
        "mark", description=mark_info, help=mark_info, add_help=True
    )

    # mark subparser arguments
    parser_mark.add_argument(
        "-p",
        "--mp",
        default=None,
        type=float,
        required = True,
        help="Minimum corrected p-value",
    )
    parser_mark.add_argument(
        "-f",
        "--mfc",
        default=None,
        type=float,
        required = True,    
        help="Minimum log2 fold-change",
    )
    parser_mark.add_argument(
        "-g",
        "--gs",
        default=None,
        type=int,
        required = True,    
        help="Maximum number of genes shared",
    )
    parser_mark.add_argument(
        "-o",
        "--output",
        default=None,
        type=str,
        required = True,    
        help="Output path",
    )
    parser_mark.add_argument(
        'deg',
        metavar='deg.txt',
        type=str,
        help='Path to deg.txt file to extract markers from'
    )



    if len(sys.argv) == 1:
        parser.print_help()
        
    args = parser.parse_args()


    # ec index
    if args.command == 'index':
        ec_index(args.groups, args.targets, args.ec, args.markers)
        
    # ec verify
    if args.command == 'verify':
        ec_verify(args.groups, args.targets, args.ec, args.markers)

    #ec merge
    if args.command == 'merge':
        ec_merge(args.markers_1, args.markers_2, args.output, args.method)
        
    if args.command == 'mark':
        ec_mark(args.mp, args.mfc, args.gs, args.output, args.deg)
    

if __name__ == "__main__":
    main()