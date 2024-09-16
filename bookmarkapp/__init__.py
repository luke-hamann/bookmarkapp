"""
    Title: Application Initializer
    Authors: Malachi Harris & Luke Hamann
    Date: 2024-08-31
    Updated: 2024-09-13
    Purpose: Create and configure the application object for Flask
"""

import tomllib
from flask import Flask, render_template
from bookmarkapp.auth import get_user, get_csrf_token
from bookmarkapp.controller import controller


# Initialize the Flask application.
# used to define routes, handle requests, and configure application
app = Flask("bookmarkapp")


# Opens config.toml to set configuration variables
try:
    with open('config.toml', 'rb') as f:
        app.config.update(tomllib.load(f))
except FileNotFoundError:
    exit()


# Create blueprint used for routing
app.register_blueprint(controller)


# Error handlers for expected HTTP errors
# Renders custom error page w/ title and message
@app.errorhandler(401)
def unauthorized(error):
    return render_template("error.html", user=get_user(),
                           title="401 Unauthorized",
                           message="You are not authorized to perform this action.",
                           csrf_token=get_csrf_token()), 401

@app.errorhandler(403)
def internal_server_error(error):
    return render_template("error.html", user=get_user(),
                           title="403 Forbidden",
                           message="You don't have the permission to access the requested resource. It is either read-protected or not readable by the server.",
                           csrf_token=get_csrf_token()), 500

@app.errorhandler(404)
def not_found(error): 
    return render_template("error.html", user=get_user(),
                           title="404 Not Found",
                           message="That page does not exist.",
                           csrf_token=get_csrf_token()), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return render_template("error.html", user=get_user(),
                           title="405 Method Not Allowed",
                           message="This page cannot be accessed that way.",
                           csrf_token=get_csrf_token()), 405

@app.errorhandler(500)
def internal_server_error(error):
    return render_template("error.html", user=get_user(),
                           title="500 Internal Server Error",
                           message="Something went wrong on our end.",
                           csrf_token=get_csrf_token()), 500
