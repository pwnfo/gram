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
            usage_str = c.get_usage()
            log.info(
                f"gram {encoder[0]:<10} # {c.complete_name}"
                + (f"  [ {usage_str} ]" if usage_str else "")
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

                parsed_kwargs = {}
                for key, val in extra_options.items():
                    expected_type = getattr(Encoder, "options", {}).get(key)
                    if expected_type is None:
                        log.error(f"error: '{key}' is not a valid option.")
                        return 1
                    
                    try:
                        if isinstance(expected_type, (list, tuple, set)):
                            if val not in expected_type:
                                log.error(f"error: '{key}' must be [{'|'.join(expected_type)}].")
                                return 1
                            parsed_kwargs[key] = val
                        elif expected_type is bool:
                            if not isinstance(val, bool):
                                log.error(f"error: '{key}' does not expect a value.")
                                return 1
                            parsed_kwargs[key] = val
                        else:
                            if isinstance(val, bool) and val is True:
                                log.error(f"error: '{key}' requires a value.")
                                return 1
                            parsed_kwargs[key] = expected_type(val)
                    except (ValueError, TypeError):
                        log.error(f"error: '{key}' must be {expected_type.__name__}.")
                        return 1

                e = Encoder(
                    data,
                    **parsed_kwargs,
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
