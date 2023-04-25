from fastapi import FastAPI, APIRouter, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from kova.db import get_session
from kova.db.models import User

router = APIRouter()


class RegisterPostModel(BaseModel):
    email: EmailStr


@router.post("/register")
async def register_user(
    payload: RegisterPostModel,
    session: AsyncSession = Depends(get_session),
):
    query = await session.execute(
        select(User).where(User.email == payload.email)
    )
    user = query.one()

    return user


def app_maker():
    app = FastAPI(version="1.0.0")
    app.include_router(router=router)

    return app
