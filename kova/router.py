import warnings
from collections import deque, defaultdict
from typing import Type, TypeAlias, Callable, Any

from nats.aio.client import Client as NATSClient
from nats.aio.msg import Msg as NATSMsg

from .types import Message, Reply, Publish


class Context:
    pass


class InMemoryQueue:
    def __init__(self):
        self._messages = defaultdict(deque)

    async def messages(self, subject: str):
        while True:
            q = self._messages[subject]
            if q:
                yield q.pop()
            else:
                break

    async def publish(self, subject: str, payload: bytes):
        self._messages[subject].append(payload)


Queue: TypeAlias = NATSClient | InMemoryQueue
MessageType: TypeAlias = Type[Message]


class Router:
    def __init__(self, queue: Queue | None = None):
        self.routes: dict[str, list[Callable]] = defaultdict(list)
        self.queue = queue

    def bind(self, queue: Queue):
        self.queue = queue

    async def dispatch(self, subject: str, msg: NATSMsg):
        if self.queue is None:
            raise RuntimeError("Router not bound to a queue")

        async def publish(subject: str, payload: bytes):
            await self.queue.publish(  # type: ignore
                subject=subject, payload=payload
            )

        async def reply(payload: bytes):
            await publish(subject=msg.reply, payload=payload)

        message_parsed_as = None

        for route in self.routes.get(subject, []):
            kwargs: dict[str, Any] = {}

            for attr, atype in route.__annotations__.items():
                if issubclass(atype, Publish):
                    kwargs[attr] = publish

                elif issubclass(atype, Reply):
                    if msg.reply:
                        kwargs[attr] = reply
                    else:
                        kwargs[attr] = None

                elif issubclass(atype, Message):
                    if message_parsed_as:
                        warnings.warn(
                            f"There is only one message per handler call, "
                            f"and {message_parsed_as} has already "
                            f"been defined as the unmarshalling type. "
                            f"You might want to check if "
                            f"using {atype} is also necessary."
                        )
                    else:
                        message_parsed_as = atype
                    message = atype.FromString(msg.data)
                    kwargs[attr] = message

            await route(**kwargs)

    def subscribe(self, subject: str):
        def wrapper(func):
            self.routes[subject].append(func)
            return func

        return wrapper
