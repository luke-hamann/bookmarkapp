import tomllib
from flask import Flask, render_template
from .auth import get_user
from .controller import controller

app = Flask("bookmarkapp")

try:
    app.config.from_file('../config.toml', load=tomllib.load, text=False)
except FileNotFoundError:
    print('config.toml not found.')
    exit()

app.register_blueprint(controller)

@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", user=get_user(),
                           title="404 Not Found",
                           message="That page does not exist."), 404

@app.errorhandler(500)
def server_error(error):
    return render_template("error.html", user=get_user(),
                           title="500 Server Error",
                           message="Something went wrong on our end."), 500
