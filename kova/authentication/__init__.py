from fastapi import FastAPI, APIRouter, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session
import re

from kova.db import get_session
from kova.db.models import User
from kova.generate_jwt import create_creds


router = APIRouter()


class RegisterPostModel(BaseModel):
    email: EmailStr


class LoginPostModel(BaseModel):
    email: EmailStr


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
        raise ValueError("Email already registerd")

    return user


@router.post("/login")
async def login_user(
    payload: LoginPostModel,
    session: Session = Depends(get_session),
):

    query = session.execute(select(User.id).where(User.email == payload.email))
    user = query.one_or_none()

    if user is None:
        raise ValueError("Email not registerd")
    else:
        look_for_id = re.search(
            "(?<=(ULID\\())[a-zA-Z0-9]*(?=[\\)])", user.__str__()
        )
        if look_for_id is not None:
            id = look_for_id.group()
        credentials = create_creds(id)
        print(credentials)

    return user.__str__()


def app_maker():
    app = FastAPI(version="1.0.0")
    app.include_router(router=router)

    return app
