import secrets
from flask import Flask
from .controller import controller

app = Flask("bookmarkapp")
app.config.update(
    SECRET_KEY=secrets.token_hex()
)
app.register_blueprint(controller)
