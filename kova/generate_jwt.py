import subprocess
import os

from kova.settings import get_settings


def create_creds(ULID):
    if ULID is not None:
        pub = f"{ULID}.>"
        sub = "_INBOX.>"

        subprocess.run(
            [
                "nsc",
                "add",
                "user",
                "--name",
                ULID,
                "--allow-pub",
                pub,
                "--allow-sub",
                sub,
                "--expiry",
                "6M",
            ],
            capture_output=True,
            text=True,
        )
        settings = get_settings()
        filename = f"{ULID}.creds"

        path = settings.nats_creds_directory + "/" + filename

        file = open(path, mode="r")
        f = file.read()
        os.remove(path)
    else:
        raise ValueError("ULID can't be None")
    return f
