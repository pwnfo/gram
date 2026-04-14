import re
import typing

from ast import literal_eval
from gram.encoders.registry import register
from gram.encoders.base import Encoder


def decode_point_format(data: str) -> str:
    def repl(m: re.Match) -> str:
        code_point = int(m.group(1), 16)

        return chr(code_point)

    return re.sub(r"[U|u]\+([0-9A-Fa-f]{4,8})\s?", repl, data)


@register
class UnicodeEncoder(Encoder):
    name = "unicode"
    complete_name = "Unicode Escape"
    options = {"format": ("short", "long", "point"), "lower": bool}

    def __init__(
        self, stream: typing.IO[bytes], encoding: str = "utf-8", **kwargs: typing.Any
    ):
        super().__init__(stream, encoding, **kwargs)

    def encode(self) -> typing.Iterator[bytes | str]:
        fmt: str | None = self.kwargs.get("format", None)
        lower: bool = self.kwargs.get("lower", False)

        for line in self.stream:
            data = line.decode(self.encoding)
            res = ""
            for char in data:
                if fmt == "short":
                    res += f"\\u{ord(char):04X}"
                elif fmt == "long":
                    res += f"\\U{ord(char):08X}"
                elif fmt == "point":
                    res += f"U+{ord(char):04X} "
                else:
                    if ord(char) < 0x10000:
                        res += f"\\u{ord(char):04X}"
                    else:
                        res += f"\\U{ord(char):08X}"

            if lower:
                res = res.lower()

            if fmt == "point":
                res = res.rstrip()

            yield res

    def decode(self) -> typing.Iterator[bytes | str]:
        for line in self.stream:
            data = line.decode(self.encoding)
            if "U+" in data.upper():
                res = ""
                for m in re.finditer(r"U\+([0-9A-Fa-f]+)", data, re.IGNORECASE):
                    res += chr(int(m.group(1), 16))
                yield res
            else:
                data = data.replace("\\U", "\\U").replace("\\u", "\\u")
                safe_str = f'"{data}"'
                try:
                    yield literal_eval(safe_str)
                except Exception:
                    yield data


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(UnicodeEncoder, "Hêllo Wôrld")
