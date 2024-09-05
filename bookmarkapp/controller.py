from flask import abort, Blueprint, render_template, session
from bookmarkapp.models import Database, User

controller = Blueprint('controller', __name__, url_prefix='/')

# Helper functions

def get_user() -> User:
    userId = session.get('userId', None)
    if (userId is None):
        return None
    else:
        return Database.get_user(userId)

def set_user(user: User) -> None:
    if (user is None):
        session['userId'] = None
    else:
        session['userId'] = user.id

# Readonly Views

@controller.route("/", methods=['GET'])
def index():
    try:
        bookmarks = Database.get_all_bookmarks()
    except:
        abort(500)

    return render_template("index.html", bookmarks=bookmarks, user=get_user(),
                           return_url="/")
