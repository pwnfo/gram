from gram.encoders.registry import register
from gram.encoders.base import Encoder
from typing import Any

import base64


@register
class Base64Encoder(Encoder):
    name = "b64"
    complete_name = "Base64"
    usage = "-f lbreak=[mime|pem]"

    def __init__(self, data: bytes, encoding: str = "utf-8", **kwargs: Any):
        self.data = data
        self.encoding = encoding

        self.lbreak = kwargs.get("lbreak")
        if isinstance(self.lbreak, str):
            self.lbreak = self.lbreak.lower()

    def encode(self) -> str:
        result = base64.b64encode(self.data).decode(self.encoding)
        if self.lbreak == "pem":
            return "\n".join(result[i : i + 64] for i in range(0, len(result), 64))
        if self.lbreak == "mime":
            return "\n".join(result[i : i + 76] for i in range(0, len(result), 76))

        return result

    def decode(self) -> bytes:
        return base64.b64decode(self.data)


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(Base64Encoder, "Hello World")
