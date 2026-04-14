from gram.encoders.registry import register
from gram.encoders.base import Encoder
import urllib.parse

import typing


def quote_full(content: str, encoding: str = "utf-8") -> str:
    return "".join(f"%{b:02X}" for b in content.encode(encoding))


@register
class URLEncoder(Encoder):
    name = "url"
    complete_name = "URL Encoding"
    options = {"plus": bool, "full": bool}

    def __init__(
        self, stream: typing.IO[bytes], encoding: str = "utf-8", **kwargs: typing.Any
    ):
        super().__init__(stream, encoding, **kwargs)

    def encode(self) -> typing.Iterator[bytes | str]:
        plus: bool = self.kwargs.get("plus", False)
        full: bool = self.kwargs.get("full", False)

        for line in self.stream:
            data = line.decode(self.encoding)
            if full:
                res = ""
                for char in data:
                    res += "%%%02x" % ord(char)
                yield res
            elif plus:
                yield urllib.parse.quote_plus(data)
            else:
                yield urllib.parse.quote(data)

    def decode(self) -> typing.Iterator[bytes | str]:
        plus: bool = self.kwargs.get("plus", False)

        for line in self.stream:
            data = line.decode(self.encoding)
            if plus:
                yield urllib.parse.unquote_plus(data)
            else:
                yield urllib.parse.unquote(data)


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(URLEncoder, "&Hello World?")
