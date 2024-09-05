from functools import wraps
from flask import abort, Blueprint, redirect, render_template, request, url_for
from .models import Bookmark, Database, ExceptionList
from .auth import get_user, set_user

controller = Blueprint('controller', __name__, url_prefix='/')

# Helper functions

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

@controller.route("/", methods=['GET'])
def index():
    try:
        bookmarks = Database.get_all_bookmarks()
    except:
        abort(500)

    return render_template("index.html", bookmarks=bookmarks, user=get_user(),
                           return_url="/")

@controller.route("/<int:id>", methods=['GET'])
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

@controller.route("/add", methods=["GET", "POST"])
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

@controller.route("/<int:id>/edit", methods=["GET", "POST"])
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

@controller.route("/<int:id>/delete", methods=["GET", "POST"])
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

    return redirect(url_for('controller.index'))

# Authentication

@controller.route("/login", methods=["GET", "POST"])
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
        if (return_url.startswith('//') or not return_url.startswith('/')):
            return_url = '/'

        try:
            user = Database.authenticate_user(username, password)
        except ExceptionList as e:
            return render_template("login.html", errors=e.error_list, return_url=return_url)

        set_user(user)
        return redirect(return_url)

@controller.route("/logout", methods=["GET", "POST"])
def logout():
    if (request.method == 'POST'):
        set_user(None)
    return redirect(url_for('controller.index'))
