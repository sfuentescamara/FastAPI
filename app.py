from flask import Flask, request

import config

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World'


if __name__ == "__main__":
    app.run(host="localhost", port=config.PORT, debug=config.DEBUG_MODE)