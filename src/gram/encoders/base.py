from abc import ABC, abstractmethod
from typing import Any


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
        self,
        data: bytes,
        encoding: str = "utf-8",
        **kwargs: Any,
    ):
        self.data = data
        self.encoding = encoding
        self.kwargs = kwargs

    @abstractmethod
    def encode(self) -> str | bytes:
        pass

    @abstractmethod
    def decode(self) -> str | bytes:
        pass
