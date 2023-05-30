# Copyright 2016-2020 The NATS Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
import asyncio
import sys

import nats

from kova.protocol.ping_pb2 import EchoRequest, EchoResponse


def show_usage():
    usage = """
nats-pub [-s SERVER] <subject> <data>

Example:

nats-pub -s demo.nats.io greeting 'Hello World'
"""
    print(usage)


def show_usage_and_die():
    show_usage()
    sys.exit(1)


async def run():
    parser = argparse.ArgumentParser()

    # e.g. nats-pub -s demo.nats.io hello "world"
    parser.add_argument("subject", default="hello", nargs="?")
    parser.add_argument("-d", "--data", default="ping")
    parser.add_argument("-s", "--servers", default="nats://localhost:4222")
    parser.add_argument("--creds", default="")
    parser.add_argument("--queue", default="")
    parser.add_argument("--ping", default=False, action="store_true")
    args, unknown = parser.parse_known_args()

    data = args.data
    if len(unknown) > 0:
        data = unknown[0]

    async def error_cb(e):
        print("Error:", e)

    async def reconnected_cb():
        print("Got reconnected to NATS...")

    async def subscribe_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print(
            "Received a message on '{subject} {reply}': {data}".format(
                subject=subject, reply=reply, data=data
            )
        )
        await msg.respond(b"pong")

    options = {"error_cb": error_cb, "reconnected_cb": reconnected_cb}

    if len(args.creds) > 0:
        options["user_credentials"] = args.creds

    try:
        if len(args.servers) > 0:
            options["servers"] = args.servers

        nc = await nats.connect(**options)
    except Exception as e:
        print(e)
        show_usage_and_die()

    req = EchoRequest()
    req.message = data
    payload = req.SerializeToString()

    if args.ping:
        response = await nc.request(args.subject, payload, timeout=10)
        print(f"Send message [{args.subject}] : '{data}'")
        res = EchoResponse.FromString(response.data)
        print(f"Got response: {res.message}")
    else:
        await nc.subscribe(args.subject, cb=subscribe_handler)

    await nc.flush()
    await nc.drain()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(run())
    except RuntimeError:
        print("RuntimeError")
    finally:
        loop.close()
