import secrets

from flask import Flask

app = Flask("bookmarkapp")
app.config.update(
    SECRET_KEY=secrets.token_hex()
)

import bookmarkapp.controller
