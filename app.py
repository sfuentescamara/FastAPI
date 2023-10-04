import config
import os

debug = config.DEBUG_MODE

def create_fast_api(app):
    from api.api import myFastApi
    api = myFastApi(app)
    return api

def create_flask_api(app):
    from api.api import myFlaskApi
    api = myFlaskApi(app)
    return api

def init_app():
    if config.fast_api:
        if debug:
            print("Initializing fastapi")
        from fastapi import FastAPI
        app = FastAPI()
        api = create_fast_api(app)
        while 1:
            pass
    else:
        if debug:
            print("Initializing flask api")
        from flask import Flask
        app = Flask(__name__)
        api = create_flask_api(app)


if __name__ == "__main__":
    init_app()
