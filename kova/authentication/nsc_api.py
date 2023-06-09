from fastapi import FastAPI, APIRouter, Depends
from functools import lru_cache
from typing import List

from pydantic import BaseModel, BaseSettings
from pathlib import Path

from kova.authentication.nsc import NscWrapper

import uvicorn

nsc_router = APIRouter()

ENV_FILE = ".env"


class NscSettings(BaseSettings):
    class Config:
        env_prefix = "nsc_"
        env_file = ENV_FILE

    app_name: str = "NSC service"
    nsc_path: str = "nsc"
    nats_creds_directory: str
    operator_name: str | None = None
    account_name: str | None = None
    expiry: str = "6M"
    allow_pub: List[str] | None = None
    allow_sub: List[str] = ["_INBOX.>"]

    def data_dir(self):
        return (Path(self.nats_creds_directory) / "stores").as_posix()

    def keystore_dir(self):
        return (Path(self.nats_creds_directory) / "keys").as_posix()


@lru_cache()
def get_nsc_settings() -> NscSettings:
    settings = NscSettings()
    return settings


class SetUpPostModel(BaseModel):
    operator: str
    account: str


class CreateUserPostModel(BaseModel):
    name: str
    account: str | None = None


class NscAPIException(Exception):
    pass


@nsc_router.get("/info")
async def info(
    settings: NscSettings = Depends(get_nsc_settings),
):
    return {
        "app_name": settings.app_name,
        "nsc_files": settings.nats_creds_directory,
        "data_dir": settings.data_dir(),
        "keystore_dir": settings.keystore_dir(),
    }


@nsc_router.post("/new-setup")
def set_up_operator_account(
    payload: SetUpPostModel,
    settings: NscSettings = Depends(get_nsc_settings),
):
    nsc = NscWrapper(
        nsc_path=settings.nsc_path,
        data_dir=settings.data_dir(),
        keystore_dir=settings.keystore_dir(),
    )

    nsc.create_operator(name=payload.operator)
    nsc.create_account(name=payload.account)

    return nsc.get_account_jwt(operator=payload.operator, name=payload.account)


@nsc_router.post("/new-user")
def create_user(
    payload: CreateUserPostModel,
    settings: NscSettings = Depends(get_nsc_settings),
):
    nsc = NscWrapper(
        nsc_path=settings.nsc_path,
        data_dir=settings.data_dir(),
        keystore_dir=settings.keystore_dir(),
    )

    account = ""
    if payload.account is None and settings.account_name is None:
        raise NscAPIException("No Account Provided")
    elif payload.account is not None:
        account = payload.account
    elif settings.account_name is not None:
        account = settings.account_name

    if settings.operator_name is None:
        raise NscAPIException("No Operator Provided")

    pub = [f"{payload.name}.>"]
    if settings.allow_pub is not None:
        pub.extend(settings.allow_pub)

    nsc.create_user(
        name=payload.name,
        allow_pub=",".join(pub),
        allow_sub=",".join(settings.allow_sub),
        expiry=settings.expiry,
        account=account,
    )

    creds = nsc.get_user_credentials(
        name=payload.name, account=account, operator=settings.operator_name
    )
    return creds


def nsc_app_maker():
    app = FastAPI(version="1.0.0")
    app.include_router(router=nsc_router)

    return app


if __name__ == "__main__":
    app = nsc_app_maker()
    uvicorn.run(app, port=4000, host="0.0.0.0")
