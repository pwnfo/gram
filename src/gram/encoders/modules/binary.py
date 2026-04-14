from gram.encoders.registry import register
from gram.encoders.base import Encoder
from typing import Any


@register
class BinaryEncoder(Encoder):
    name = "bin"
    complete_name = "Binary String"
    options = {"sep": int}

    def __init__(self, data: bytes, encoding: str = "utf-8", **kwargs: Any):
        self.data = data
        self.encoding = encoding
        self.separator = kwargs.get("sep", 0)

    def encode(self) -> str:
        result = "".join(format(c, "08b") for c in self.data)
        if self.separator:
            return " ".join(
                result[i : i + self.separator]
                for i in range(0, len(result), self.separator)
            )
        return result

    def decode(self) -> bytes:
        self.data = self.data.replace(b" ", b"").strip()

        return bytes(int(self.data[i : i + 8], 2) for i in range(0, len(self.data), 8))


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(BinaryEncoder, "Hello World")
