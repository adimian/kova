import dataclasses

import pytest

from kova.protocol.login_pb2 import LoginRequest
from kova.router import Publish, Reply
from kova.server import Router


@dataclasses.dataclass
class Msg:
    subject: str = ""
    reply: str = ""
    data: bytes = b""
    headers: dict[str, str] | None = None


@pytest.mark.asyncio
async def test_handler_can_be_defined_for_route():
    router = Router()

    @router.route("test.handler", message_type=LoginRequest)
    async def handle_login(message, reply: Reply):
        if reply:
            await reply(f"hello {message.email}".encode())

    assert router.routes["test.handler"][0].__name__ == "handle_login"


@pytest.mark.asyncio
async def test_router_can_evaluate_messages(queue):
    router = Router(queue=queue)

    req = LoginRequest()
    req.email = "hello@acme.test"

    @router.route("test.handler", message_type=LoginRequest)
    async def handle_login(
        message: LoginRequest,
        reply: Reply,
        publish: Publish,
    ):
        if reply:
            await reply(f"hello {message.email}".encode())
        publish("security.audit", f"{message.email} just logged in".encode())

    await router.dispatch(
        subject="test.handler",
        msg=Msg(
            data=req.SerializeToString(),
            subject="test.handler",
            reply="_INBOX.test.handler",
        ),
    )

    msg = await anext(queue.messages("_INBOX.test.handler"))
    assert msg == b"hello hello@acme.test"

    msg = await anext(queue.messages("security.audit"))
    assert msg == b"hello@acme.test just logged in"
