from . import __version__
import argparse
import sys
import logging
from .ec_check import setup_ec_check_args, validate_ec_check_args
from .ec_clean import setup_ec_clean_args, validate_ec_clean_args
from .ec_convert import setup_ec_convert_args, validate_ec_convert_args
from .ec_index import setup_ec_index_args, validate_ec_index_args
from .ec_mark import setup_ec_mark_args, validate_ec_mark_args
from .ec_merge import setup_ec_merge_args, validate_ec_merge_args
from .ec_verify import setup_ec_verify_args, validate_ec_verify_args
from .ec_filter import setup_ec_filter_args, validate_ec_filter_args


def main():
    # setup parsers
    parser = argparse.ArgumentParser(description=f"ec {__version__}: handle ec files")
    parser.add_argument(
        "--verbose", help="Print debugging information", action="store_true"
    )
    subparsers = parser.add_subparsers(
        dest="command",
        metavar="<CMD>",
    )

    # Setup the arguments for all subcommands
    command_to_parser = {
        "check": setup_ec_check_args(subparsers),
        "clean": setup_ec_clean_args(subparsers),
        "convert": setup_ec_convert_args(subparsers),
        "index": setup_ec_index_args(subparsers),
        "mark": setup_ec_mark_args(subparsers),
        "merge": setup_ec_merge_args(subparsers),
        "verify": setup_ec_verify_args(subparsers),
        "filter": setup_ec_filter_args(subparsers),
    }

    # Show help when no arguments are given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    if len(sys.argv) == 2:
        if sys.argv[1] in command_to_parser:
            command_to_parser[sys.argv[1]].print_help(sys.stderr)
        else:
            parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # setup logging
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)7s %(message)s",
        level=logging.DEBUG if args.verbose else logging.INFO,
    )

    # Setup validator and runner for all subcommands (validate and run if valid)
    COMMAND_TO_FUNCTION = {
        "check": validate_ec_check_args,
        "clean": validate_ec_clean_args,
        "convert": validate_ec_convert_args,
        "index": validate_ec_index_args,
        "mark": validate_ec_mark_args,
        "merge": validate_ec_merge_args,
        "verify": validate_ec_verify_args,
        "filter": validate_ec_filter_args,
    }
    COMMAND_TO_FUNCTION[sys.argv[1]](parser, args)


if __name__ == "__main__":
    main()
