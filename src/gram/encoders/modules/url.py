from gram.encoders.registry import register
from gram.encoders.base import Encoder
from typing import Any

from urllib.parse import quote, unquote, quote_plus, unquote_plus


@register
class URLEncoder(Encoder):
    name = "url"
    complete_name = "URL Encoding"
    usage = "-f plus"

    def __init__(self, data: bytes, encoding: str = "utf-8", **kwargs: Any):
        self.data = data
        self.encoding = encoding

        self.text = data.decode(self.encoding)
        self.plus = kwargs.get("plus")

    def encode(self) -> str:
        if self.plus:
            return quote_plus(self.text)

        return quote(self.text)

    def decode(self) -> str:
        if self.plus:
            return unquote_plus(self.text)

        return unquote(self.text)


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(URLEncoder, "&Hello World?")
