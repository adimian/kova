"""
    This server serves back messages sent to `test.echo.cached`
    The reply will be the same for 5 seconds, after which it will be updated
"""
from kova.protocol.ping_pb2 import EchoRequest, EchoResponse
from kova.server import Server, Router
from kova.cache import Cache
from kova.message import Reply

from arrow import now

router = Router()


@router.subscribe("test.echo.cached")
async def cache_request(msg: EchoRequest, cache: Cache, reply: Reply):
    key = msg.message
    resp = await cache.get(key)
    if resp is None:
        payload = EchoResponse()
        payload.message = f"echo {msg.message} from {now().isoformat()}"
        resp = payload.SerializeToString()
        await cache.set(key, resp, ttl=5)

    await reply(resp)


server = Server()
server.add_router(router=router)
server.run()
