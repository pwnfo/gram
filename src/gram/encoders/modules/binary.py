from gram.encoders.registry import register
from gram.encoders.base import Encoder

import typing


@register
class BinaryEncoder(Encoder):
    name = "bin"
    complete_name = "Binary String"
    options = {"sep": int}

    def __init__(
        self, stream: typing.IO[bytes], encoding: str = "utf-8", **kwargs: typing.Any
    ):
        super().__init__(stream, encoding, **kwargs)
        self.separator = kwargs.get("sep", 0)

    def encode(self) -> typing.Iterator[bytes | str]:
        sep: int | None = self.kwargs.get("sep", None)

        while True:
            chunk = self.stream.read(4000)
            if not chunk:
                break

            result = ""
            for byte in chunk:
                result += bin(byte)[2:].zfill(8)

            if sep is not None:
                res = []
                for i in range(0, len(result), sep):
                    res.append(result[i : i + sep])
                result = " ".join(res)

            yield result

    def decode(self) -> typing.Iterator[bytes | str]:
        data_full = self.stream.read().decode(self.encoding)
        data_full = data_full.replace(" ", "").strip()

        if data_full.startswith("0b"):
            data_full = data_full[2:]

        n = int(data_full, 2)
        yield n.to_bytes((n.bit_length() + 7) // 8, "big")


if __name__ == "__main__":
    from gram.encoders.modules import test_encoder

    test_encoder(BinaryEncoder, "Hello World")
