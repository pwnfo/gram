from gram.encoders.registry import register
from gram.encoders.base import Encoder
from typing import Any

from html import escape, unescape


def full_escape(content: str) -> str:
    return "".join(f"&#{ord(c)};" for c in content)


@register
class HTMLEncoder(Encoder):
    name = "html"
    complete_name = "HTML Escape"
    usage = "-f full"

    def __init__(self, data: bytes, encoding: str = "utf-8", **kwargs: Any):
        self.data = data
        self.encoding = encoding

        self.text = data.decode(self.encoding)
        self.full = kwargs.get("full") is not None

    def encode(self) -> str:
        if self.full:
            return full_escape(self.text)
        return escape(self.text)

    def decode(self) -> str:
        return unescape(self.text)


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(HTMLEncoder, "<Hello World />")
