# Router

Each queue is linked to a router which describe how the applicative server processes the messages of the queue.

````python
from kova.protocol.ping_pb2 import EchoRequest, EchoResponse
from kova.router import Router

from kova.message import Reply
from loguru import logger

router = Router()


@router.subscribe("*.echo")
async def echo(msg: EchoRequest, reply: Reply):
    logger.debug(f"Received message: '{msg.message}'")
    if reply:
        res = EchoResponse()
        res.message = f"echo {msg.message}"
        await reply(res.SerializeToString())
        logger.debug("Response sent")
    else:
        logger.warning("Unable to reply")

````

This router listens on the `*.echo` queue. It will receive an EchoRequest and if the message needs a Reply will answer with an EchoResponse.
The echo function will be called everytime a message is processed on the `*.echo` queue.
