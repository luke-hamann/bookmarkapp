from functools import wraps
from flask import abort, redirect, render_template, request, session, url_for
from bookmarkapp import app
from bookmarkapp.models import Bookmark, Database, ExceptionList, User

# Helper functions

def get_user() -> User:
    userId = session.get('userId', None)
    if userId is None:
        return None
    else:
        return Database.get_user(userId)

def set_user(user: User) -> None:
    if user is None:
        session.pop('userId')
    else:
        session['userId'] = user.id

def login_required(old_function):
    @wraps(old_function)
    def new_function(*args, **kwargs):
        if get_user() is None:
            return redirect(f"/login?return_url={request.path}")
        return old_function(*args, **kwargs)
    
    return new_function

def get_bookmark_from_form() -> Bookmark:
    title = request.form.get('title', '')
    url = request.form.get('url', '')
    blurb = request.form.get('blurb', '')
    description = request.form.get('description', '')
    return Bookmark(1, title, url, blurb, description)

# Readonly Views

@app.route("/", methods=['GET'])
def index():
    try:
        bookmarks = Database.get_all_bookmarks()
    except:
        abort(500)

    return render_template("index.html", bookmarks=bookmarks, user=get_user(),
                           return_url="/")

@app.route("/<int:id>", methods=['GET'])
def detail(id):
    try:
        bookmark = Database.get_bookmark(id)
    except:
        abort(500)

    if bookmark is None:
        abort(404)
    
    return render_template("detail.html", bookmark=bookmark,
                           return_url=request.path, user=get_user())

# Form Views

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "GET":
        title = request.args.get('title', '')
        url = request.args.get('url', '')
        blurb = request.args.get('blurb', '')
        description = request.args.get('description', '')

        return render_template("add.html", bookmark=None, user=get_user(),
                               return_url=request.path
        )
    else:
        try:
            bookmark = get_bookmark_from_form()
            bookmark = Database.add_bookmark(bookmark, get_user())
        except ExceptionList as e:
            return render_template(
                "add.html",
                bookmark=bookmark,
                errors=e.error_list,
                user=get_user(),
                return_url=request.path
            )

        return redirect(bookmark.id)

@app.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit(id):
    if request.method == "GET":
        bookmark = Database.get_bookmark(id)
        if bookmark is None:
            abort(404)

        return render_template(
            "edit.html",
            bookmark=bookmark,
            errors=None,
            user=get_user()
        )
    else:
        bookmark = get_bookmark_from_form()
        bookmark.id = id

        try:
            Database.update_bookmark(bookmark, get_user())
        except ExceptionList as e:
            return render_template(
                "edit.html",
                bookmark=bookmark,
                errors=e.error_list,
                user=get_user()
            )
        
        return redirect(f'/{id}')

@app.route("/<int:id>/delete", methods=["GET", "POST"])
@login_required
def delete(id):
    bookmark = Database.get_bookmark(id)
    if bookmark is None:
        abort(404)

    if request.method == 'GET':
        return render_template(
            "delete.html",
            bookmark=bookmark, 
            user=get_user())
    
    Database.delete_bookmark(bookmark, get_user())

    return redirect(url_for('index'))

# Authentication

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return_url = request.args.get('return_url', '/')
        if (not return_url.startswith('/')):
            return_url = '/'

        if (get_user() is None):
            return render_template("login.html", return_url=return_url)
        else:
            return redirect(return_url)
        
    else:
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        return_url = request.form.get('return_url', '/')
        if (not return_url.startswith('/')):
            return_url = '/'

        try:
            user = Database.authenticate_user(username, password)
        except ExceptionList as e:
            return render_template("login.html", errors=e.error_list, return_url=return_url)

        set_user(user)
        return redirect(return_url)

@app.route("/logout", methods=["GET", "POST"])
def logoff():
    if (request.method == 'GET'):
        return redirect('index')
    else:
        set_user(None)
        return redirect(url_for('index'))

# Error Pages

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
