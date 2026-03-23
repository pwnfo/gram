from gram.encoders.registry import register
from gram.encoders.base import Encoder
from typing import Any

import quopri


@register
class QuotedPrintableEncoder(Encoder):
    name = "quopri"
    complete_name = "Quoted-printable"

    def __init__(self, data: bytes, encoding: str = "utf-8", **kwargs: Any):
        self.data = data
        self.encoding = encoding

    def encode(self) -> str:
        return quopri.encodestring(self.data).decode(self.encoding)

    def decode(self) -> bytes:
        return quopri.decodestring(self.data)


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(QuotedPrintableEncoder, "Hêllo Wôrld")
