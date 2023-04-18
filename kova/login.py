from kova.protocol.login_pb2 import LoginRequest, LoginResponse
from kova.router import Router
from kova.our_types import Reply
from loguru import logger
import subprocess

router = Router()


@router.subscribe("test.login")
async def login(msg: LoginRequest, reply: Reply):
    logger.debug(f"received message: {msg.email}")
    if reply:
        res = LoginResponse()
        completed_process = subprocess.run(
            ["nsc", "describe", "account", "-F", "name"],
            capture_output=True,
            text=True,
        )
        res.account_name = completed_process.stdout
        logger.debug(res.account_name)
        await reply(res.SerializeToString())
        logger.debug("response sent")
    else:
        logger.warning("unable to reply")
