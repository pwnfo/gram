import sys
import argparse

from gram import __description__, __author__, __version__
from gram.logger import log

from typing import Never


class GramParser(argparse.ArgumentParser):
    def error(self, message: str) -> Never:
        self.print_usage(sys.stderr)
        sys.stderr.write("\n")
        log.error(message)
        sys.exit(1)


def parse_key_value(opt: str) -> dict:
    value: str | bool

    if "=" in opt:
        key, value = opt.split("=", 1)
    else:
        key, value = opt, True

    return {key: value}


def create_parser(prog: str = "gram") -> GramParser:
    parser = GramParser(
        prog=prog,
        add_help=False,
        usage=f"{prog} <encoder> [options]",
        description=__description__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Use 'gram list' to see all available encoders.",
    )
    options = parser.add_argument_group()

    options.add_argument("-h", action="help", help="show this help message and exit")
    options.add_argument(
        "-v",
        action="version",
        version=f"Gram v{__version__} (Python {sys.version_info.major}.{sys.version_info.minor})",
        help="show version message and exit",
    )
    options.add_argument("-d", dest="decode", action="store_true", help="decode input")
    options.add_argument(
        "-b",
        action="store_true",
        dest="bline",
        help="append trailing newline to output",
    )
    options.add_argument(
        "-o",
        metavar="file",
        dest="output",
        help="file to write output to",
    )
    options.add_argument(
        "-f",
        metavar="option",
        action="append",
        dest="extra",
        type=parse_key_value,
        help="extra options for encoders",
    )
    options.add_argument(
        "-s",
        metavar="string",
        dest="string",
        help="string to encode (does not use stdin)",
    )
    options.add_argument(
        "-e",
        metavar="encoding",
        dest="encoding",
        help="select text encoding (default: 'utf-8')",
        default="utf-8",
    )

    parser.add_argument("encoder", nargs="?", help=argparse.SUPPRESS)

    return parser
