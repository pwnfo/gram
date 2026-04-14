from gram.encoders.registry import register
from gram.encoders.base import Encoder

import typing


@register
class HexadecimalEncoder(Encoder):
    name = "hex"
    complete_name = "Hexadecimal String"
    options = {"sep": int, "upper": bool}

    def __init__(
        self, stream: typing.IO[bytes], encoding: str = "utf-8", **kwargs: typing.Any
    ):
        super().__init__(stream, encoding, **kwargs)
        self.separator = kwargs.get("sep", 0)
        self.uppercase = kwargs.get("upper", False)

    def encode(self) -> typing.Iterator[bytes | str]:
        sep: int | None = self.kwargs.get("sep", None)
        upper: bool = self.kwargs.get("upper", False)

        while True:
            chunk = self.stream.read(4096)
            if not chunk:
                break

            result = chunk.hex()
            if sep is not None:
                res = []
                for i in range(0, len(result), sep):
                    res.append(result[i : i + sep])
                result = " ".join(res)

            if upper:
                result = result.upper()

            yield result

    def decode(self) -> typing.Iterator[bytes | str]:
        data = self.stream.read().replace(b" ", b"").strip()

        yield bytes.fromhex(data.decode(self.encoding))


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(HexadecimalEncoder, "Hello World")
