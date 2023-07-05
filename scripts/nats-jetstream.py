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
    parser.add_argument("-d", "--data", default="hello world")
    parser.add_argument("-s", "--servers", default="nats://localhost:4222")
    parser.add_argument("--creds", default="")
    parser.add_argument("--token", default="")
    parser.add_argument("--request", default=False, action="store_true")
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

    if args.token.strip() != "":
        options["token"] = args.token.strip()

    try:
        if len(args.servers) > 0:
            options["servers"] = args.servers

        nc = await nats.connect(**options)
        js = nc.jetstream()
    except Exception as e:
        print(e)
        show_usage_and_die()

    async def message_handler(msg):
        res = EchoResponse.FromString(msg.data)
        print(f"Got response: '{res.message}'")

    await js.add_stream(
        name="test", subjects=[args.subject, f"{args.subject}.reply"]
    )
    await js.subscribe(f"{args.subject}.reply", cb=message_handler)

    req = EchoRequest()
    req.message = data
    payload = req.SerializeToString()

    await js.publish(args.subject, payload)
    print(f"Published on [{args.subject}] : '{data}'")

    await js.purge_stream("test")
    await js.delete_stream("test")

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
