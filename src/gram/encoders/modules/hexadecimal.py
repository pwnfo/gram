from gram.encoders.registry import register
from gram.encoders.base import Encoder
from typing import Any


@register
class HexadecimalEncoder(Encoder):
    name = "hex"
    complete_name = "Hexadecimal String"
    options = {"sep": int, "upper": bool}

    def __init__(self, data: bytes, encoding: str = "utf-8", **kwargs: Any):
        self.data = data
        self.encoding = encoding
        self.separator = kwargs.get("sep", 0)
        self.uppercase = kwargs.get("upper", False)

    def encode(self) -> str:
        result = self.data.hex()

        if self.uppercase:
            result = result.upper()

        if self.separator:
            return " ".join(
                result[i : i + self.separator]
                for i in range(0, len(result), self.separator)
            )

        return result

    def decode(self) -> bytes:
        self.data = self.data.replace(b" ", b"").strip()

        return bytes.fromhex(self.data.decode(self.encoding))


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(HexadecimalEncoder, "Hello World")
