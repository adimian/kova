import pytest

from kova.protocol.login_pb2 import LoginRequest
from kova.server import Router
from kova.our_types import Msg
from kova.message import Publish, Reply


@pytest.mark.asyncio
async def test_handler_can_be_defined_for_route():
    router = Router()

    @router.subscribe("test.handler")
    async def handle_login():
        pass

    assert router.handlers["test.handler"][0].__name__ == "handle_login"


@pytest.mark.asyncio
async def test_router_can_evaluate_messages(queue):
    router = Router(queue=queue)

    req = LoginRequest()
    req.email = "hello@acme.test"

    @router.subscribe("test.handler")
    async def handle_login(
        message: LoginRequest,
        reply: Reply,
        publish: Publish,
    ):
        if reply:
            await reply(f"hello {message.email}".encode())
        await publish(
            "security.audit",
            f"{message.email} just logged in".encode(),
        )

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
