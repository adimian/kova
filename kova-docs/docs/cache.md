# Cache

Cache entries have :

- a payload
- an expiry timestamp (Optional)

## Add message to Cache
A message is composed of a byte array. It can be set in cache with a key (str) and a time to live (ttl) in seconds. This ttl is optional.

```python
from kova.cache import Cache

cache = Cache()
key = "hello"
message = b"good morning!"
await cache.set(key, message, ttl=5)
```

## Get message from Cache

A message then can be retrieved from the cache thanks to its key.

````python
resp = await cache.get(key)
# resp == b"good morning!"
````
## Use with an applicative server

In the caching echo example, the `Cache` is used to store a message in cache in the `Router`.
The response message will be stored for 5 second in cache before being sent.

````python
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
````
