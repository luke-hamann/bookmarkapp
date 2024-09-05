import secrets
from flask import Flask, render_template
from .auth import get_user
from .controller import controller

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
def server_error(error):
    return render_template("error.html", user=get_user(),
                           title="500 Server Error",
                           message="Something went wrong on our end."), 500
