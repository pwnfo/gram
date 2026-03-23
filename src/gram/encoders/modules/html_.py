from gram.encoders.registry import register
from gram.encoders.base import Encoder
from typing import Any

from html import escape, unescape


@register
class HTMLEncoder(Encoder):
    name = "html"
    complete_name = "HTML Escape"

    def __init__(self, data: bytes, encoding: str = "utf-8", **kwargs: Any):
        self.data = data
        self.encoding = encoding

        self.text = data.decode(self.encoding)

    def encode(self) -> str:
        return escape(self.text)

    def decode(self) -> str:
        return unescape(self.text)


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(HTMLEncoder, "<Hello World />")
