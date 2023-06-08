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
