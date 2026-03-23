from gram.encoders.base import Encoder

encoders: dict[str, type[Encoder]] = {}


def register(cls: type[Encoder]) -> type[Encoder]:
    encoders[cls.name] = cls

    return cls
