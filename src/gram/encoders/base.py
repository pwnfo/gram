from abc import ABC, abstractmethod

import typing


class Encoder(ABC):
    name: str
    complete_name: str
    options: dict[str, type | tuple[str, ...]] = {}

    @classmethod
    def get_usage(cls) -> str | None:
        if not cls.options:
            return None
        parts = []
        for key, expected_type in cls.options.items():
            if isinstance(expected_type, (list, tuple, set)):
                parts.append(f"-f {key}=[{'|'.join(expected_type)}]")
            elif expected_type is bool:
                parts.append(f"-f {key}")
            else:
                parts.append(f"-f {key}=N")
        return " ".join(parts)

    def __init__(
        self, stream: typing.IO[bytes], encoding: str = "utf-8", **kwargs: typing.Any
    ):
        self.stream = stream
        self.encoding = encoding
        self.kwargs = kwargs

        for key, value in kwargs.items():
            setattr(self, key, value)

    @abstractmethod
    def encode(self) -> typing.Iterator[bytes | str]:
        pass

    @abstractmethod
    def decode(self) -> typing.Iterator[bytes | str]:
        pass
