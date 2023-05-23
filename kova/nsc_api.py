from fastapi import FastAPI, APIRouter
import tempfile

from pydantic import BaseModel, BaseSettings, Field
from pathlib import Path

from kova.authentication.nsc import NscWrapper

nsc_router = APIRouter()


def _get_default_nsc_creds_directory():
    tmp = Path(tempfile.gettempdir()) / "nsc-creds"
    tmp.mkdir(exist_ok=True)
    return tmp.as_posix()


class NscSettings(BaseSettings):
    app_name: str = "NSC service"
    nats_creds_directory: str = Field(
        default_factory=_get_default_nsc_creds_directory
    )


settings = NscSettings()


class SetUpPostModel(BaseModel):
    operator: str
    account: str


@nsc_router.post("/new-setup")
def set_up_operator_account(
    payload: SetUpPostModel,
):
    nsc = NscWrapper(
        nsc_path="nsc",
        data_dir=(Path(settings.nats_creds_directory) / "stores").as_posix(),
        keystore_dir=(Path(settings.nats_creds_directory) / "keys").as_posix(),
    )

    nsc.create_operator(name=payload.operator)
    nsc.create_account(name=payload.account)

    return nsc.get_operator_jwt(payload.operator)


def nsc_app_maker():
    app = FastAPI(version="1.0.0")
    app.include_router(router=nsc_router)

    return app
