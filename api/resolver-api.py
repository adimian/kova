from fastapi import FastAPI, Response

app = FastAPI()

accounts = [
    {"id": 1, "name": "John"},
    {"id": 2, "name": "Phillip"},
]


@app.get("/")
def test():
    return {"ça fonctionne ?": "maybe"}


@app.get("/home")
def index():
    return {"message": "Hello World"}


@app.get("/accounts")
def get_accounts():
    # TODO : get all the files and give them
    return accounts


@app.get("/accounts/{id}")
def get_account(id: int, response: Response):
    for account in accounts:
        if account["id"] == id:
            return account
    response.status_code = 404
    return "Product Not found"


@app.post("/accounts")
def create_account(account: dict, response: Response):
    account["id"] = len(accounts) + 1
    accounts.append(account)
    response.status_code = 201
    return account
