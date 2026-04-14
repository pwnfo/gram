from gram.encoders.registry import register
from gram.encoders.base import Encoder
import typing

import codecs


@register
class PunycodeEncoder(Encoder):
    name = "puny"
    complete_name = "Punycode IDN"

    def __init__(
        self, stream: typing.IO[bytes], encoding: str = "utf-8", **kwargs: typing.Any
    ):
        super().__init__(stream, encoding, **kwargs)

    def encode(self) -> typing.Iterator[bytes | str]:
        for line in self.stream:
            data = line.decode(self.encoding)
            yield codecs.encode(data, "punycode")

    def decode(self) -> typing.Iterator[bytes | str]:
        for line in self.stream:
            data = line.decode(self.encoding)
            yield codecs.decode(data.encode("ascii"), "punycode")


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(PunycodeEncoder, "hêllô-wõrld.com")
