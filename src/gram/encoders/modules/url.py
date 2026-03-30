from gram.encoders.registry import register
from gram.encoders.base import Encoder
from typing import Any

from urllib.parse import quote, unquote, quote_plus, unquote_plus


def quote_full(content: str, encoding: str = "utf-8") -> str:
    return "".join(f"%{b:02X}" for b in content.encode(encoding))


@register
class URLEncoder(Encoder):
    name = "url"
    complete_name = "URL Encoding"
    usage = "-f plus -f full"

    def __init__(self, data: bytes, encoding: str = "utf-8", **kwargs: Any):
        self.data = data
        self.encoding = encoding

        self.text = data.decode(self.encoding)
        self.plus = kwargs.get("plus")
        self.full = kwargs.get("full") is not None

    def encode(self) -> str:
        if self.full:
            return quote_full(self.text, encoding=self.encoding)
        if self.plus:
            return quote_plus(self.text, encoding=self.encoding)

        return quote(self.text, encoding=self.encoding)

    def decode(self) -> str:
        if self.plus:
            return unquote_plus(self.text, encoding=self.encoding)

        return unquote(self.text, encoding=self.encoding)


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(URLEncoder, "&Hello World?")
