from fastapi import FastAPI


def app_maker():
    app = FastAPI(version="1.0.0")

    return app
