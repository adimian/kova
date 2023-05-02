import subprocess

from kova.settings import get_settings


def create_creds(ULID):
    if ULID is not None:
        pub = f"{ULID}.*"
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
            ],
            capture_output=True,
            text=True,
        )
        settings = get_settings()
        filename = f"{ULID}.creds"

        path = settings.nats_creds_directory + "/" + filename

        file = open(path, mode="r")
        f = file.read()
    else:
        f = None
    return f
