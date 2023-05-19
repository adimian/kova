from fastapi import FastAPI, HTTPException
import uvicorn
from loguru import logger
import subprocess
import os
import tempfile

from pydantic import BaseSettings, Field
from pathlib import Path


def _get_default_nsc_creds_directory():
    tmp = Path(tempfile.gettempdir()) / "nsc-creds"
    tmp.mkdir(exist_ok=True)
    return tmp.as_posix()


class NscSettings(BaseSettings):
    app_name: str = "NSC service"
    nsc_files: str
    nats_creds_directory: str = Field(
        default_factory=_get_default_nsc_creds_directory
    )

    class Config:
        env_file = ".env"


settings = NscSettings()
nsc_app = FastAPI()


def associate_operator():
    filesList = os.listdir(settings.nsc_files)

    operator_name = filesList[0]

    result_association = subprocess.run(
        ["nsc", "env", "-o", operator_name],
        capture_output=True,
        text=True,
        shell=True,
    )

    if result_association.stderr:
        logger.error(f"Error: {result_association.stderr}")
        raise HTTPException(
            status_code=409,
            detail=f"Couldn't add operator : {result_association.stderr}",
        )
    # logger.info(f"Info: {result_association.stdout}")

    return operator_name


def create_key_dir():
    command = f'export NKEYS_PATH="{settings.nats_creds_directory}"'

    subprocess.run(
        command,
        capture_output=True,
        text=True,
        shell=True,
    )

    result_key_dir = subprocess.run(
        ["nsc", "keys", "migrate"],
        capture_output=True,
        text=True,
        shell=True,
    )

    if result_key_dir.stderr:
        logger.error(f"Error: {result_key_dir.stderr}")
        raise HTTPException(
            status_code=409,
            detail=f"Couldn't change keys directory : {result_key_dir.stderr}",
        )
    # logger.info(f"Info: {result_test.stdout}")

    return settings.nats_creds_directory


def create_creds(ulid):
    if ulid is not None:
        pub = f"{ulid}.>"
        sub = "_INBOX.>"

        command_creation = (
            f"nsc add user --name {ulid} "
            f"--allow-pub {pub}"
            f" --allow-sub {sub} "
            f"--expiry 6M "
        )

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
        # os.remove(path)
    else:
        raise ValueError("ULID can't be None")
    return f


@nsc_app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "nsc_files": settings.nsc_files,
    }


@nsc_app.get("/operator")
def new_user():
    ulid = 2
    associate_operator()
    create_key_dir()
    credentials = create_creds(ulid)
    return credentials


if __name__ == "__main__":
    uvicorn.run("create_user:nsc_app", port=4000, reload=True, host="0.0.0.0")
