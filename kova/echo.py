from kova.protocol.ping_pb2 import EchoRequest, EchoResponse
from kova.router import Router
from kova.our_types import Reply
from loguru import logger

router = Router()


@router.subscribe("test.echo")
async def echo(msg: EchoRequest, reply: Reply):
    logger.debug(f"received message: {msg.message}")
    if reply:
        res = EchoResponse()
        res.message = f"echo {msg.message}"
        await reply(res.SerializeToString())
        logger.debug("response sent")
    else:
        logger.warning("unable to reply")
