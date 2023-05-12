"""
    This server serves back messages sent to `*.echo.identified`
    The reply will be the same for 5 seconds, after which it will be updated

    $ python scripts/nats-pub.py --request test.echo.cached

"""

from loguru import logger

from kova.protocol.ping_pb2 import EchoRequest, EchoResponse
from kova.server import Server, Router
from kova.current_user import CurrentUser
from kova.message import Reply


router = Router()


@router.subscribe("*.echo.identified")
async def identified_request(
    msg: EchoRequest, current_user: CurrentUser, reply: Reply
):
    logger.debug(f"received message: {msg.message}")
    if reply:
        res = EchoResponse()
        res.message = f"echo {msg.message} from {current_user._name}"
        await reply(res.SerializeToString())
        logger.debug("response sent")
    else:
        logger.warning("unable to reply")


server = Server()
server.add_router(router=router)
server.run()
