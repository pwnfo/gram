from abc import ABC, abstractmethod
from typing import Any


class Encoder(ABC):
    name: str
    complete_name: str
    usage: str | None = None

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
