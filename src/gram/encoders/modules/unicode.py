import re

from gram.encoders.registry import register
from gram.encoders.base import Encoder
from typing import Any


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

    def __init__(self, data: bytes, encoding: str = "utf-8", **kwargs: Any):
        self.data = data
        self.encoding = encoding
        self.format = kwargs.get("format")
        self.lower = kwargs.get("lower", False)

        self.text = data.decode(self.encoding)

    def encode(self) -> str:
        _ = "X"
        if self.lower:
            _ = "x"

        match self.format:
            case "short":
                result = "".join(f"\\u{ord(c):04{_}}" for c in self.text)
            case "point":
                result = " ".join(f"U+{ord(c):04{_}}" for c in self.text)
            case "long":
                result = "".join(f"\\U{ord(c):08{_}}" for c in self.text)
            case _:
                result = "".join(f"\\x{b:02{_}}" for b in self.data)

        return result

    def decode(self) -> str:
        if self.format != "point":
            return (
                self.data.decode("unicode_escape")
                .encode("latin1")
                .decode(self.encoding)
            )

        return decode_point_format(self.text)


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(UnicodeEncoder, "Hêllo Wôrld")
