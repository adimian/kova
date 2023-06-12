# Client

A client is the code called by users and describe their behavior

Two examples are included here :

- Nats - Pub client
- Ping - Pong client

## Connection to NATS server

The client is connected to the NATS server. Options such as the server address or the user credentials can be provided.
The connection is established through `nats.connect`.

````python
import argparse
import asyncio

import nats

async def run():
    parser = argparse.ArgumentParser()

    parser.add_argument("subject", default="hello", nargs="?")
    parser.add_argument("-d", "--data", default="hello world")
    parser.add_argument("-s", "--servers", default="nats://localhost:4222")
    parser.add_argument("--creds", default="")
    args, unknown = parser.parse_known_args()

    data = args.data
    if len(unknown) > 0:
        data = unknown[0]

    async def error_cb(e):
        print("Error:", e)

    async def reconnected_cb():
        print("Got reconnected to NATS...")

    options = {"error_cb": error_cb, "reconnected_cb": reconnected_cb}

    if len(args.creds) > 0:
        options["user_credentials"] = args.creds

    try:
        if len(args.servers) > 0:
            options["servers"] = args.servers

        nc = await nats.connect(**options)
    except Exception as e:
        print(e)
````

## Publish / Subscribe

A client can publish on a subject as well as subscribe to one to receive the messages going through this subject.

We use `protobuf` messages to allow for more flexibility in the message content when publishing (see [Messages example](messages.md) for further details).
In the following example, `EchoRequest` is a type of protobuf message. Since NATS payload are bytes array, the protobuf messages are converted to bytes.

```python
    req = EchoRequest()
    req.message = data
    payload = req.SerializeToString()

    await nc.publish(args.subject, payload)
    print(f"Published on [{args.subject}] : '{data}'")
```

A client can subscribe to a subject and will then receive all the messages related to it.
A client can define a message handler that describes how each messages received needs to be handled.

````python
    async def message_handler(msg):
        req = EchoRequest.FromString(msg.data)
        print(f"Received a message on [{msg.subject}]: '{req.message}'")

    await nc.subscribe(args.subject, cb=message_handler)
    print(f"Listening for message on [{args.subject}]")
````

##Request / Reply
A client can request an answer from the applicative server. In this case, it will use the request/reply pattern instead of the publish/subscribe one.

Once again, a message is sent by the client. The applicative server will process it (see [Router example](router.md) for further details) and send back a Response.

````python
    req = EchoRequest()
    req.message = data
    payload = req.SerializeToString()

    response = await nc.request(args.subject, payload, timeout=10)
    print(f"Requested on [{args.subject}] : '{data}'")
    res = EchoResponse.FromString(response.data)
    print(f"Got response: '{res.message}'")
````
