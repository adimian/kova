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
