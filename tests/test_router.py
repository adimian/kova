import dataclasses

import pytest

from kova.protocol.login_pb2 import LoginRequest
from kova.router import Handler, Context, Publish, Reply
from kova.server import Router
from kova.types import Message


class PrintHandler(Handler):
    async def __call__(
        self,
        context: Context,
        message: Message,
        reply: Reply,
        publish: Publish,
    ):
        print(message)


@dataclasses.dataclass
class Msg:
    subject: str = ""
    reply: str = ""
    data: bytes = b""
    headers: dict[str, str] | None = None


def test_handler_can_be_defined_for_route():
    router = Router()
    route = router.add_route("test.handler", LoginRequest)
    route.add_handler(PrintHandler)


@pytest.mark.asyncio
async def test_router_can_evaluate_messages(ctx, queue):
    req = LoginRequest()
    req.email = "hello@acme.test"

    class TestLoginHandler(Handler):
        async def __call__(
            self,
            context: Context,
            message: LoginRequest,  # type: ignore[override]
            reply: Reply,
            publish: Publish,
        ):
            if reply:
                await reply(f"hello {message.email}".encode())

    router = Router(queue=queue)
    route = router.add_route("test.handler", LoginRequest)
    route.add_handler(TestLoginHandler)

    await route(
        context=ctx,
        msg=Msg(
            data=req.SerializeToString(),
            subject="test.handler",
            reply="_INBOX.test.handler",
        ),
    )

    msg = await anext(queue.messages("_INBOX.test.handler"))
    assert msg == b"hello hello@acme.test"
