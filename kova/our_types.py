import abc
import dataclasses
from typing import TypeAlias, Type

import google.protobuf.message as _message

Message: TypeAlias = _message.Message


class Dependable(abc.ABC):
    _instances: list[Type["Dependable"]] = []

    @classmethod
    def register(cls, instance: Type["Dependable"]):
        cls._instances.append(instance)

    @classmethod
    def get_instances(cls) -> list[Type["Dependable"]]:
        return cls._instances

    @classmethod
    @abc.abstractmethod
    def get_instance(cls, *, router, subject, msg):
        raise NotImplementedError()


@dataclasses.dataclass
class Msg:
    """used in unit-testing context to simulate NATS messages"""

    subject: str = ""
    reply: str = ""
    data: bytes = b""
    headers: dict[str, str] | None = None
