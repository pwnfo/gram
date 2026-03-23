from gram.encoders.registry import register
from gram.encoders.base import Encoder
from typing import Any

import base64


@register
class Ascii85Encoder(Encoder):
    name = "a85"
    complete_name = "Ascii85"

    def __init__(self, data: bytes, encoding: str = "utf-8", **kwargs: Any):
        self.data = data
        self.encoding = encoding

    def encode(self) -> str:
        return base64.a85encode(self.data).decode(self.encoding)

    def decode(self) -> bytes:
        return base64.a85decode(self.data)


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(Ascii85Encoder, "Hello World")
