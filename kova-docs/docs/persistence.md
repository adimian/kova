# Persistent messaging

Persistence is used on both server side and client side to prevent messages from being lost.

## NATS Jetstream

NATS possesses a persistence module called JetStream  that can be enabled on the NATS server.
On the client side, it uses stream (group of queue) to send messages.

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
        js = nc.jetstream()
    except Exception as e:
        print(e)
````
A client can still subscribe to different subject.

````python
    async def message_handler(msg):
        res = EchoResponse.FromString(msg.data)
        print(f"Got response: '{res.message}'")

    await js.add_stream(
        name=current_user, subjects=[args.subject, f"{args.subject}.reply"]
    )
    await js.subscribe(f"{args.subject}.reply", cb=message_handler)
````

Because of the properties of Jetstream messaging, the Request/Reply messaging pattern is replaced by a Publish/Reply.
The client is subscribed to a dedicated reply queue `user_name.*.reply` which will receive the Server replies.

````python
    req = EchoRequest()
    req.message = data
    payload = req.SerializeToString()

    await jetstream.publish(subject, payload)
    print(f"Published on [{subject}] : '{payload.decode()}'")
````

## Message buffer

In case a client is disconnected or crash before the messages are sent, a `Buffer` is used to save the messages.
This `Buffer` uses a `sqlite3` DB to save the messages content in chronological order on the user's machine.

It can :
- `save` messages
- `get` the oldest saved message
- `get_all` messages
- `delete` a specific message
- `remove` the oldest saved message

In our `stream-echo` example that features the use of a buffer, it is used to retrieve unsent messages as well as save messages.

````python
async def send_message(jetstream, data: str, subject: str):
    buffer = Buffer(subject=subject)
    payload = buffer.get()
    if payload is None:
        req = EchoRequest()
        req.message = data
        payload = req.SerializeToString()
        name_file = buffer.save(payload)

        await jetstream.publish(subject, payload)
        print(f"Published on [{subject}] : '{payload.decode()}'")

        buffer.delete_message(name_file)
    else:
        await jetstream.publish(subject, payload)
        print(f"Published on [{subject}] : '{payload.decode()}'")
````
