import subprocess
import os

from kova.settings import get_settings


def create_creds(ulid):
    if ulid is not None:
        pub = f"{ulid}.>"
        sub = "_INBOX.>"
        settings = get_settings()

        subprocess.run(
            [
                "nsc",
                "add",
                "user",
                "--name",
                ulid,
                "--allow-pub",
                pub,
                "--allow-sub",
                sub,
                "--expiry",
                "6M",
                "--data-dir",
                settings.nats_creds_directory,
                "--keystore-dir",
                settings.nats_creds_directory,
            ],
            capture_output=True,
            text=True,
            cwd=settings.nats_creds_directory,
        )

        filename = f"{ulid}.creds"
        path = os.path.join(settings.nats_creds_directory, filename)

        with open(path) as my_jwt:
            f = my_jwt.read()
        os.remove(path)
    else:
        raise ValueError("ULID can't be None")
    return f
