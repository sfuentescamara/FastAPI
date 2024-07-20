import os
import app.config as config

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from flask import Flask
import uvicorn

from typing import Dict, List, Any


# def list_files_with_name(filename):
#     res = []

#     dirs = [paths.script_path] + [ext.path for ext in extensions.active()]

#     for dirpath in dirs:
#         if not os.path.isdir(dirpath):
#             continue

#         path = os.path.join(dirpath, filename)
#         if os.path.isfile(path):
#             res.append(path)

#     return res

def javascript_html():
    # Ensure localization is in `window` before scripts
    head = f'<script type="text/javascript"></script>\n'

    script_js = os.path.join(".", "script.js")
    head += f'<script type="text/javascript" src="{script_js}"></script>\n'

    # for script in scripts.list_scripts("javascript", ".js"):
    #     head += f'<script type="text/javascript" src="{webpath(script.path)}"></script>\n'

    # for script in scripts.list_scripts("javascript", ".mjs"):
    #     head += f'<script type="module" src="{webpath(script.path)}"></script>\n'

    # if shared.cmd_opts.theme:
    #     head += f'<script type="text/javascript">set_theme(\"{shared.cmd_opts.theme}\");</script>\n'

    return head


def css_html():
    head = ""

    def stylesheet(fn):
        return f'<link rel="stylesheet" property="stylesheet" href="{fn}">'

    # for cssfile in scripts.list_files_with_name("style.css"):
    #     if not os.path.isfile(cssfile):
    #         continue

    #     head += stylesheet(cssfile)

    # if os.path.exists(os.path.join(data_path, "user.css")):
    #     head += stylesheet(os.path.join(data_path, "user.css"))

    return head


class myFlaskApi():

    def __init__(self, app: Flask, debug :bool=False) -> None:
        self.app = app
        self.debug = debug
  
        @self.app.route('/')
        def home():
            return "Hello World"

        @self.app.route('/index')
        def index():
            # render_template()
            return 'index.html'

        self.run()

    def run(self):
        self.app.run(host=config.listen, port=config.PORT, debug=config.DEBUG_MODE)

class myFastApi:
    def __init__(self, app: FastAPI, debug :bool=False) -> None:
        self.app = app
        self.debug = debug
        self.templates = Jinja2Templates(directory="templates")
        self.add_api_route("/hi", self.hi, methods=["GET"])
        self.add_api_route("/", self.index, methods=["GET"])
        self.run()

    def add_api_route(self, path: str, endpoint, **kwargs):
        return self.app.add_api_route(path, endpoint, **kwargs)
    
    def home(self):
        if self.debug:
            print("AT HOME")
        js = javascript_html()
        css = css_html()
    
    async def index(self, request: Request):
        messege = "messege python variable!"
        return self.templates.TemplateResponse("index.html", {"request": request, "messege": messege})


    

    def hi(self):
        return {"message": "Hello World"}

    def run(self):
        uvicorn.run(self.app, host=config.listen, port=config.PORT, root_path=f"")