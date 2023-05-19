from fastapi import FastAPI, Response
from fastapi.responses import PlainTextResponse
import os
import uvicorn
import argparse
from loguru import logger

resolver_api = FastAPI()


def look_up_accounts(path_jwt):
    accounts = []
    temp_accounts = os.listdir(path_jwt)
    for account in temp_accounts:
        filename, ext = os.path.splitext(account)
        accounts.append(filename)
    return accounts


def write_jwt(path_jwt: str, jwt: str, account: str):
    filename = f"{account}.jwt"
    path = os.path.join(path_jwt, filename)
    with open(path) as my_jwt:
        my_jwt.write(jwt)


@resolver_api.get("/")
def test():
    return {"message": "Hello World"}


@resolver_api.get("/accounts")
def get_accounts():
    return look_up_accounts(opt.pathToJWT)


@resolver_api.get("/accounts/{id}", response_class=PlainTextResponse)
def get_account(id: str, response: Response):
    try:
        filename = f"{id}.jwt"
        path = os.path.join(opt.pathToJWT, filename)
        contents = open(path).read()
        contents = contents.strip()
        return contents

    except Exception as e:
        logger.error(f"Error: {e}")
        response.status_code = 404
        return "Account Not found"


@resolver_api.post("/accounts")
def create_account(account: str, jwt: str, response: Response):
    write_jwt(opt.pathToJWT, jwt, account)
    response.status_code = 201
    return "Account created"


if __name__ == "__main__":
    param = argparse.ArgumentParser()
    param.add_argument(
        "--pathToJWT",
        type=str,
        default="",
        help="The path to the JWT files on your computer",
    )
    opt = param.parse_args()

    uvicorn.run(resolver_api, port=8000, host="0.0.0.0")
