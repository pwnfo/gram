from gram.encoders.registry import register
from gram.encoders.base import Encoder

import typing
import quopri


def full_encode(content: bytes) -> str:
    return "".join(f"={b:02X}" for b in content)


@register
class QuotedPrintableEncoder(Encoder):
    name = "quopri"
    complete_name = "Quoted-printable"
    options = {"full": bool}

    def __init__(
        self, stream: typing.IO[bytes], encoding: str = "utf-8", **kwargs: typing.Any
    ):
        super().__init__(stream, encoding, **kwargs)

    def encode(self) -> typing.Iterator[bytes | str]:
        for chunk in iter(lambda: self.stream.read(4000), b""):
            yield quopri.encodestring(chunk)

    def decode(self) -> typing.Iterator[bytes | str]:
        for chunk in iter(lambda: self.stream.read(4000), b""):
            yield quopri.decodestring(chunk)


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(QuotedPrintableEncoder, "Hêllo Wôrld")
