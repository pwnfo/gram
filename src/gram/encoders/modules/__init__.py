import io

from gram.encoders.base import Encoder


def test_encoder(encoder: type[Encoder], phrase: str, encoding: str = "utf-8") -> None:
    e = encoder(io.BytesIO(phrase.encode(encoding)), encoding=encoding)
    r = e.encode()

    if not isinstance(r, str):
        r = r.decode(encoding)  # type: ignore

    print(f"'{phrase}' ({encoder.name}) -> {r}")

    e = encoder(io.BytesIO(r.encode(encoding)), encoding=encoding)

    x = e.decode()

    if not isinstance(x, str):
        x = x.decode(encoding)  # type: ignore

    print(f"'{x}' ({encoder.name}) <- {r}")
