from kova.protocol.ping_pb2 import EchoRequest
from kova.router import Router
from loguru import logger

router = Router()


@router.subscribe(">")
async def listen_all(msg: EchoRequest):
    logger.debug(f"received message: {msg.message}")
