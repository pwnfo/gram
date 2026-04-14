from gram.encoders.registry import register
from gram.encoders.base import Encoder

import typing
import base64


@register
class Base32Encoder(Encoder):
    name = "b32"
    complete_name = "Base32"

    def __init__(
        self, stream: typing.IO[bytes], encoding: str = "utf-8", **kwargs: typing.Any
    ):
        super().__init__(stream, encoding, **kwargs)

    def encode(self) -> typing.Iterator[bytes | str]:
        while True:
            chunk = self.stream.read(4000)
            if not chunk:
                break
            yield base64.b32encode(chunk).decode(self.encoding)

    def decode(self) -> typing.Iterator[bytes | str]:
        data = self.stream.read()
        yield base64.b32decode(data)


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(Base32Encoder, "Hello World")
