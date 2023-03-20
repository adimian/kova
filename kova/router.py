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
            raise RuntimeError("router not bound to a queue")

        for route in self.routes.get(subject, []):
            kwargs: dict[str, Any] = {}

            for attr, atype in route.__annotations__.items():
                if issubclass(atype, Publish):

                    async def publish(subject: str, payload: bytes):
                        await self.queue.publish(  # type: ignore
                            subject=subject, payload=payload
                        )

                    kwargs[attr] = publish

                elif issubclass(atype, Reply):
                    if msg.reply:

                        async def reply(payload: bytes):
                            await publish(subject=msg.reply, payload=payload)

                    else:
                        reply = None  # type: ignore

                    kwargs[attr] = reply

                elif issubclass(atype, Message):
                    message = atype.FromString(msg.data)
                    kwargs[attr] = message

            await route(**kwargs)

    def subscribe(self, subject: str):
        def wrapper(func):
            self.routes[subject].append(func)

        return wrapper
