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
import requests
import argparse
import asyncio
import sys
import os

import nats

from kova.protocol.image_pb2 import (
    ImageRequest,
    ImageResponse,
    ModifiedImageResponse,
    ImageConfirmation,
)


def show_usage():
    usage = """
python clients/client_send_file.py -s <server> --creds <credentials>
--destination <client> --data <image> <subject>


Example:

python clients/client_send_file.py -s demo.nats.io
--data path/to/image.png test.send_file
"""
    print(usage)


def show_usage_and_die():
    show_usage()
    sys.exit(1)


async def run():
    parser = argparse.ArgumentParser()

    parser.add_argument("subject", default="hello", nargs="?")
    parser.add_argument("-d", "--data", default="./lenna.png")
    parser.add_argument("--transformation", default="*.transform_file")
    parser.add_argument("-s", "--servers", default="nats://localhost:4222")
    parser.add_argument("--creds", default="")
    parser.add_argument("--token", default="")
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
    except Exception as e:
        print(e)
        show_usage_and_die()

    path, file = os.path.split(data)
    name, ext = file.split(".")

    # Ask to upload an image
    req = ImageRequest()
    req.name = name
    payload = req.SerializeToString()

    response = await nc.request(args.subject, payload, timeout=10)
    print(f"Requested on [{args.subject}] : '{file}'")

    res = ImageResponse.FromString(response.data)
    print("Got response with presigned URL")

    # Upload image with presigned URL
    with open(data, mode="rb") as f:
        byte_im = f.read()

    res = requests.put(res.URL, data=byte_im)

    if res.status_code == 200 and args.transformation:
        # Confirmation send
        req = ImageConfirmation()
        req.name = name
        payload = req.SerializeToString()

        response = await nc.request(args.transformation, payload, timeout=10)
        print(f"Requested on [{args.transformation}] : '{name}'")

        # Modified images
        res = ModifiedImageResponse.FromString(response.data)
        print("Got response: \n")
        for transformation in res.transformation:
            print(f"{transformation.name} available at {transformation.URL}\n")
    else:
        print(res.text)

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
