import subprocess
import os

from kova.settings import get_settings
from loguru import logger


def create_creds(ulid):
    if ulid is not None:
        pub = f"{ulid}.>"
        sub = "_INBOX.>"
        settings = get_settings()

        command_set_up = (
            f"nsc env -s {settings.nats_creds_directory} "
            f"-o operator-nats -a account_A"
        )
        command_creation = (
            f"nsc add user --name {ulid} "
            f"--allow-pub {pub}"
            f" --allow-sub {sub} "
            f"--expiry 6M "
            f"--keystore-dir {settings.nats_creds_directory}"
        )

        result_set_up = subprocess.run(
            command_set_up,
            capture_output=True,
            text=True,
            shell=True,
        )

        # TODO : how to get operator and account jwt in temp file
        # breakpoint()
        logger.error(f"Error: {result_set_up.stderr}")

        result_creation = subprocess.run(
            command_creation,
            capture_output=True,
            text=True,
            shell=True,
        )

        logger.error(f"Error: {result_creation.stderr}")

        filename = f"{ulid}.creds"
        path = os.path.join(settings.nats_creds_directory, filename)

        with open(path) as my_jwt:
            f = my_jwt.read()
        os.remove(path)
    else:
        raise ValueError("ULID can't be None")
    return f
