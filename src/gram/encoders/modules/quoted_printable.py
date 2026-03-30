from gram.encoders.registry import register
from gram.encoders.base import Encoder
from typing import Any

import quopri


def full_encode(content: bytes) -> str:
    return "".join(f"={b:02X}" for b in content)


@register
class QuotedPrintableEncoder(Encoder):
    name = "quopri"
    complete_name = "Quoted-printable"
    usage = "-f full"

    def __init__(self, data: bytes, encoding: str = "utf-8", **kwargs: Any):
        self.data = data
        self.encoding = encoding

        self.full = kwargs.get("full") is not None

    def encode(self) -> str:
        if self.full:
            return full_encode(self.data)
        return quopri.encodestring(self.data).decode(self.encoding)

    def decode(self) -> bytes:
        return quopri.decodestring(self.data)


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(QuotedPrintableEncoder, "Hêllo Wôrld")
