from fastapi import FastAPI, Response
from fastapi.responses import PlainTextResponse
import os
import uvicorn
import argparse

resolver_api = FastAPI()

param = argparse.ArgumentParser()
param.add_argument(
    "--pathToJWT",
    type=str,
    default="",
    help="The path to the JWT files on your computer",
)
opt = param.parse_args()


def look_up_accounts(pathToJWT):
    accounts = []
    temp_accounts = os.listdir(pathToJWT)
    for account in temp_accounts:
        accounts.append(os.path.splitext(account)[0])
    return accounts


def write_jwt(pathToJWT: str, jwt: str, account: str):
    file = open(pathToJWT + "/" + account + ".jwt", "w")
    file.write(jwt)


@resolver_api.get("/")
def test():
    return {"message": "Hello World"}


@resolver_api.get("/accounts")
def get_accounts():
    accounts = []
    accounts = look_up_accounts(opt.pathToJWT)
    return accounts


@resolver_api.get("/accounts/{id}", response_class=PlainTextResponse)
def get_account(id: str, response: Response):
    try:
        contents = open(opt.pathToJWT + "/" + id + ".jwt").read()
        print(contents)
        contents = contents.strip()
        return contents

    except Exception as e:
        print(e)
        response.status_code = 404
        return "Account Not found"


@resolver_api.post("/accounts")
def create_account(account: str, jwt: str, response: Response):
    write_jwt(opt.pathToJWT, jwt, account)
    response.status_code = 201
    return "Account created"


if __name__ == "__main__":
    uvicorn.run(resolver_api, port=8000, host="0.0.0.0")
