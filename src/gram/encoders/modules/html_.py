from gram.encoders.registry import register
from gram.encoders.base import Encoder

import typing
import html


def full_escape(content: str) -> str:
    return "".join(f"&#{ord(c)};" for c in content)


@register
class HTMLEncoder(Encoder):
    name = "html"
    complete_name = "HTML Escape"
    options = {"full": bool}

    def __init__(
        self, stream: typing.IO[bytes], encoding: str = "utf-8", **kwargs: typing.Any
    ):
        super().__init__(stream, encoding, **kwargs)
        self.full = kwargs.get("full", False)

    def encode(self) -> typing.Iterator[bytes | str]:
        for line in self.stream:
            data = line.decode(self.encoding)
            if self.full:
                res = ""
                for char in data:
                    res += f"&#{ord(char)};"
                yield res
            else:
                yield html.escape(data)

    def decode(self) -> typing.Iterator[bytes | str]:
        for line in self.stream:
            data = line.decode(self.encoding)
            yield html.unescape(data)


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(HTMLEncoder, "<Hello World />")
