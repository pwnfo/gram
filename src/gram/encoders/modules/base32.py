from gram.encoders.registry import register
from gram.encoders.base import Encoder
from typing import Any

import base64


@register
class Base32Encoder(Encoder):
    name = "b32"
    complete_name = "Base32"

    def __init__(self, data: bytes, encoding: str = "utf-8", **kwargs: Any):
        self.data = data
        self.encoding = encoding

    def encode(self) -> str:
        return base64.b32encode(self.data).decode(self.encoding)

    def decode(self) -> bytes:
        return base64.b32decode(self.data)


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(Base32Encoder, "Hello World")
