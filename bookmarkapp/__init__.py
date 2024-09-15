"""
    Title: Application Initializer
    Purpose: Create and configure the application object for Flask
"""

import tomllib
from flask import Flask, render_template
from bookmarkapp.auth import get_user, get_csrf_token
from bookmarkapp.controller import controller

app = Flask("bookmarkapp")
app.config['DEBUG'] = True

try:
    with open('config.toml', 'rb') as f:
        app.config.update(tomllib.load(f))
except FileNotFoundError:
    exit()

app.register_blueprint(controller)

@app.errorhandler(401)
def unauthorized(error):
    return render_template("error.html", user=get_user(),
                           title="401 Unauthorized",
                           message="You are not authorized to perform this action.",
                           csrf_token=get_csrf_token()), 401

@app.errorhandler(404)
def not_found(error): 
    return render_template("error.html", user=get_user(),
                           title="404 Not Found",
                           message="That page does not exist.",
                           csrf_token=get_csrf_token()), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template("error.html", user=get_user(),
                           title="500 Internal Server Error",

                           message="Something went wrong on our end."), 500
                           
@app.errorhandler(403)
def internal_server_error(error):
    return render_template("error.html", user=get_user(),
                           title="403 Forbidden",
                           message="You don't have the permission to access the requested resource. It is either read-protected or not readable by the server."),
                           csrf_token=get_csrf_token()), 500
