from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Message(BaseModel):
    message: str


@app.post("/msg")
async def update_item(payload: Message):
    return {"message": "hello"}
