from fastapi import FastAPI, APIRouter, Depends
from functools import lru_cache

from pydantic import BaseModel, BaseSettings
from pathlib import Path

from kova.authentication.nsc import NscWrapper

nsc_router = APIRouter()


class NscSettings(BaseSettings):
    app_name: str = "NSC service"
    nsc_path: str = "nsc"
    nats_creds_directory: str

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
    operator: str
    account: str
    name: str


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

    return nsc.get_operator_jwt(payload.operator)


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

    nsc.create_user(
        name=payload.name,
        allow_pub=f"{payload.name}.>",
        allow_sub="_INBOX.>",
        expiry="6M",
        account=payload.account,
    )

    creds = nsc.get_user_credentials(
        name=payload.name, account=payload.account, operator=payload.operator
    )
    return creds


def nsc_app_maker():
    app = FastAPI(version="1.0.0")
    app.include_router(router=nsc_router)

    return app
