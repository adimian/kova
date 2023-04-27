from fastapi import FastAPI, APIRouter, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session

from kova.db import get_session
from kova.db.models import User

router = APIRouter()


class RegisterPostModel(BaseModel):
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


def app_maker():
    app = FastAPI(version="1.0.0")
    app.include_router(router=router)

    return app
