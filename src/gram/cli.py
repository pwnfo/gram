import sys
import difflib

from gram.args import create_parser
from gram.logger import log
from gram.encoders.registry import encoders

from typing import Any, Iterator, IO
from contextlib import contextmanager

help_message = "use 'gram list' to see all available encoders."


@contextmanager
def s_open(file: str, mode: str = "xb", **kwargs: Any) -> Iterator[IO[Any] | None]:
    """Opens file and handles possible errors."""
    fp = None
    try:
        fp = open(file, mode, **kwargs)
        yield fp
    except PermissionError:
        log.error(f"no permission for '{file}'.")
        yield None
    except FileExistsError:
        log.error(f"file '{file}' already exists.")
        yield None
    except Exception as e:
        log.exception(f"unexpected error: {e}.")
        yield None
    finally:
        if fp:
            fp.close()


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()

    if not args.encoder:
        parser.print_usage()
        log.error(f"\n{help_message}")

        return 1

    if args.encoder == "list":
        for encoder in encoders.items():
            c = encoder[1]
            log.info(
                f"gram {encoder[0]:<10} # {c.complete_name}"
                + ("  [ %s ]" % c.usage if c.usage else "")
            )

        return 0

    extra_options = {}
    if args.extra:
        for i in args.extra:
            extra_options.update(i)

    try:
        for name, Encoder in encoders.items():
            if args.encoder == name:
                if args.string is not None:
                    data = args.string.encode(args.encoding)
                else:
                    try:
                        data = sys.stdin.buffer.read()
                    except KeyboardInterrupt:
                        return 1

                e = Encoder(
                    data,
                    **extra_options,
                    encoding=args.encoding,
                )

                if args.decode:
                    result = e.decode()
                else:
                    result = e.encode()

                if isinstance(result, str):
                    result = result.encode(args.encoding)

                result = bytes(result)

                if args.output is None:
                    sys.stdout.buffer.write(result + (b"\n" if args.bline else b""))
                    sys.stdout.flush()
                else:
                    with s_open(args.output, "xb") as fp:
                        if fp is None:
                            return 1
                        fp.write(result)
                return 0
    except Exception as err:
        log.error(f"error: {err}")
        return 1

    error_msg = f"{args.encoder}: unknown encoder."
    suggestion = difflib.get_close_matches(args.encoder, encoders.keys(), n=1)

    if suggestion:
        error_msg += f" did you mean '{suggestion[0]}'?"

    log.error(error_msg + f"\n{help_message}")

    return 1
