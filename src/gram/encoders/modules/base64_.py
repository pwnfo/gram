from gram.encoders.registry import register
from gram.encoders.base import Encoder

import typing
import base64


@register
class Base64Encoder(Encoder):
    name = "b64"
    complete_name = "Base64"
    options = {"lbreak": ("mime", "pem")}

    def __init__(
        self, stream: typing.IO[bytes], encoding: str = "utf-8", **kwargs: typing.Any
    ):
        super().__init__(stream, encoding, **kwargs)

    def encode(self) -> typing.Iterator[bytes | str]:
        lbreak: str = self.kwargs.get("lbreak", "")
        chunk_size = 24576

        while True:
            chunk = self.stream.read(chunk_size)
            if not chunk:
                break

            res = base64.b64encode(chunk).decode(self.encoding)

            if lbreak == "mime":
                res = "\n".join(res[i : i + 76] for i in range(0, len(res), 76)) + "\n"
            elif lbreak == "pem":
                res = "\n".join(res[i : i + 64] for i in range(0, len(res), 64)) + "\n"

            yield res

    def decode(self) -> typing.Iterator[bytes | str]:
        buffer = b""
        for chunk in iter(lambda: self.stream.read(8192), b""):
            buffer += chunk.replace(b"\n", b"").replace(b"\r", b"")
            valid_len = (len(buffer) // 4) * 4
            if valid_len > 0:
                valid_chunk = buffer[:valid_len]
                buffer = buffer[valid_len:]
                yield base64.b64decode(valid_chunk)
        if buffer:
            yield base64.b64decode(buffer + b"=" * ((4 - len(buffer) % 4) % 4))


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(Base64Encoder, "Hello World")
