from gram.encoders.registry import register
from gram.encoders.base import Encoder
from typing import Any


@register
class PunycodeEncoder(Encoder):
    name = "puny"
    complete_name = "Punycode IDN"

    def __init__(self, data: bytes, encoding: str = "utf-8", **kwargs: Any):
        self.data = data
        self.encoding = encoding

        self.text = data.decode(self.encoding)

    def encode(self) -> str:
        return self.text.encode("idna").decode("ascii")

    def decode(self) -> str:
        return self.text.encode("ascii").decode("idna")


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(PunycodeEncoder, "hêllô-wõrld.com")
