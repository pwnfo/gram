import io
import sys
import typing
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
                try:
                    stdin_empty = sys.stdin.isatty()
                except Exception:
                    stdin_empty = True

                if not stdin_empty and args.string is None:
                    pass
                else:
                    if not args.string:
                        log.error(
                            "error: unable to parse empty input, either pipe stdin or use the '-s' parameter."
                        )
                        parser.print_help()
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
                                log.error(
                                    f"error: '{key}' must be [{'|'.join(expected_type)}]."
                                )
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

                stream: typing.IO[bytes]
                if args.string is not None:
                    stream = io.BytesIO(args.string.encode(args.encoding))
                else:
                    stream = sys.stdin.buffer

                e = Encoder(
                    stream,
                    **parsed_kwargs,
                    encoding=args.encoding,
                )

                try:
                    iterator = e.decode() if args.decode else e.encode()

                    if not isinstance(iterator, Iterator):
                        iterator = iter([iterator])

                    if args.output is None:
                        for chunk in iterator:
                            if isinstance(chunk, str):
                                chunk = chunk.encode(args.encoding)
                            sys.stdout.buffer.write(chunk)
                        if args.bline:
                            sys.stdout.buffer.write(b"\n")
                    else:
                        with open(args.output, "wb") as fp:
                            for chunk in iterator:
                                if isinstance(chunk, str):
                                    chunk = chunk.encode(args.encoding)
                                fp.write(chunk)
                            if args.bline:
                                fp.write(b"\n")
                except KeyboardInterrupt:
                    return 1
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
