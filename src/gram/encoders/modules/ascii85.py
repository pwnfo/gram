from gram.encoders.registry import register
from gram.encoders.base import Encoder

import typing
import base64


@register
class Ascii85Encoder(Encoder):
    name = "a85"
    complete_name = "Ascii85"

    def __init__(
        self, stream: typing.IO[bytes], encoding: str = "utf-8", **kwargs: typing.Any
    ):
        super().__init__(stream, encoding, **kwargs)

    def encode(self) -> typing.Iterator[bytes | str]:
        while True:
            chunk = self.stream.read(4096)
            if not chunk:
                break
            yield base64.a85encode(chunk).decode(self.encoding)

    def decode(self) -> typing.Iterator[bytes | str]:
        data = self.stream.read()
        yield base64.a85decode(data)


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(Ascii85Encoder, "Hello World")
