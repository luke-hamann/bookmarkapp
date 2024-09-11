"""
    Title: Application Initializer
    Purpose: Create and configure the application object for Flask
"""

import secrets
from flask import Flask, render_template
from bookmarkapp.auth import get_user
from bookmarkapp.controller import controller

app = Flask("bookmarkapp")
app.config.update(
    SECRET_KEY=secrets.token_hex()
)
app.register_blueprint(controller)

@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", user=get_user(),
                           title="404 Not Found",
                           message="That page does not exist."), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template("error.html", user=get_user(),
                           title="500 Internal Server Error",
                           message="Something went wrong on our end."), 500
