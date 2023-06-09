import requests
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session

from kova.db import get_session
from kova.db.models import User

from kova.settings import get_settings


router = APIRouter()


class RegisterPostModel(BaseModel):
    email: EmailStr


class LoginPostModel(BaseModel):
    email: EmailStr


class BaseNscClient:
    def create_user(self, name: str) -> str:
        raise NotImplementedError()


class NscClient(BaseNscClient):
    def create_user(self, name: str) -> str:
        settings = get_settings()
        res = requests.post(
            f"{settings.nsc_api}/new-user", json={"name": name}
        )
        if res.status_code == 200:
            return res.json()
        raise ValueError()


class TestNscClient(BaseNscClient):
    def create_user(self, name: str) -> str:
        return f"very-serious-credentials-{name}"


def get_nsc_client() -> NscClient:
    return NscClient()


@router.post("/register")
async def register_user(
    payload: RegisterPostModel,
    session: Session = Depends(get_session),
):
    query = session.execute(select(User).where(User.email == payload.email))
    user = query.one_or_none()

    if user is None:
        user = User(email=payload.email.lower())
        session.add(user)
        session.commit()
    else:
        raise HTTPException(status_code=409, detail="Email already registered")

    return user


@router.post("/login")
async def login_user(
    payload: LoginPostModel,
    session: Session = Depends(get_session),
    nsc_client: BaseNscClient = Depends(get_nsc_client),
):
    query = session.execute(select(User.id).where(User.email == payload.email))
    user = query.one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="Email not registered")
    else:
        credentials = nsc_client.create_user(str(user.id))
    return credentials


def app_maker():
    app = FastAPI(version="1.0.0")
    app.include_router(router=router)

    return app
