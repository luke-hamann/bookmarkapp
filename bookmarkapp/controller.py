"""
    Title: Application Controller
    Purpose: Create a Flask blueprint to serve as the controller
"""

from functools import wraps
from flask import abort, Blueprint, redirect, render_template, request, url_for
from bookmarkapp.auth import get_user, set_user
from bookmarkapp.models import Bookmark, Database, ExceptionList, User
from werkzeug.security import generate_password_hash
import sqlite3
from bookmarkapp.models import Database

controller = Blueprint('controller', __name__, url_prefix='/')

# Helper functions

def login_required(old_function):
    @wraps(old_function)
    def new_function(*args, **kwargs):
        if (get_user() is None):
            return redirect(f"/login?return_url={request.path}")
        return old_function(*args, **kwargs)
    
    return new_function

def admin_permission_required(old_function):
    @wraps(old_function)
    def new_function(*args, **kwargs):
        if (get_user().privilege != 'admin'):
            abort(403)
        return old_function(*args, **kwargs)
    
    return new_function

def get_bookmark_from_form() -> Bookmark:
    title = request.form.get('title', '')
    url = request.form.get('url', '')
    blurb = request.form.get('blurb', '')
    description = request.form.get('description', '')
    return Bookmark(1, title, url, blurb, description)

def validate_return_url(return_url):
    if (return_url.startswith("//") or not return_url.startswith("/")):
        return_url = "/"
    return return_url

# Read-Only Views

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
    except ExceptionList:
        abort(404)
    except:
        abort(500)

    return render_template("detail.html", bookmark=bookmark,
                                          return_url=request.path, user=get_user())

# Form Views

@controller.route("/add", methods=["GET", "POST"])
@login_required
def add():
    #page w/ form for user to add bookmark

    
    if (request.method == "GET"):
        #initial entry: load add.html
        return render_template('add.html', bookmark=None, user=get_user(),
                                return_url=request.path)
    else:
        try:
            #on post, try to make bookmark & add to DB
            bookmark = get_bookmark_from_form()
            id = Database.add_bookmark(bookmark, get_user())
        except ExceptionList as e:
            #on failed atttempt, reload page w/ error_list
            return render_template('add.html', bookmark=bookmark,
                                   errors=e.error_list, user=get_user(),
                                   return_url=request.path)

        #on success redirect to newly created bookmark detail page
        return redirect(id)

@controller.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit(id):
    if (request.method == "GET"):
        try:
            bookmark = Database.get_bookmark(id)
        except ExceptionList:
            abort(404)
        except:
            abort(500)

        return render_template('edit.html', bookmark=bookmark, user=get_user())
    else:
        bookmark = get_bookmark_from_form()
        bookmark.id = id

        try:
            Database.update_bookmark(bookmark, get_user())
        except ExceptionList as e:
            return render_template('edit.html', bookmark=bookmark,
                                    errors=e.error_list, user=get_user())
        
        return redirect(f'/{id}')

@controller.route("/<int:id>/delete", methods=["GET", "POST"])
@login_required
def delete(id):
    try:
        bookmark = Database.get_bookmark(id)
    except ExceptionList:
        abort(404)
    except:
        abort(500)

    if (request.method == 'GET'):
        return render_template('delete.html', bookmark=bookmark,
                                user=get_user())
    else:
        try:
            Database.delete_bookmark(bookmark, get_user())
        except ExceptionList as e:
            return render_template('delete.html', bookmark=bookmark,
                                   user=get_user())

        return redirect('/')

# Authentication

@controller.route("/login", methods=["GET", "POST"])
def login():
    if (request.method == 'GET'):
        return_url = request.args.get('return_url', '/')
        return_url = validate_return_url(return_url)

        if (get_user() is None):
            return render_template("login.html", return_url=return_url)
        else:
            return redirect(return_url)
        
    else:
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        return_url = request.form.get('return_url', '/')
        return_url = validate_return_url(return_url)

        try:
            user = Database.authenticate_user(username, password)
        except ExceptionList as e:
            return render_template("login.html", errors=e.error_list,
                                   return_url=return_url, username=username)

        set_user(user)
        return redirect(return_url)

@controller.route("/logout", methods=["GET", "POST"])
def logout():
    if (request.method == 'POST'):
        set_user(None)
    return redirect(url_for('controller.index'))


# ----------------------------------------------ADDITION TO APP----------------------------------------------
# USERS LIST                VIEW METHOD
@controller.route("/users", methods=["GET", "POST"])
@admin_permission_required
def users():
    #page to allow admin to see user accounts and delete or add them

    #access DB to get user data for table
    try:
        users = Database.get_all_users_for_table()
    except ExceptionList:
        abort(404)
    # except:
    #     abort(500)

    if (request.method == "GET"):
        #initial entry: load users.html
        return render_template("users.html", users = users,
                           return_url=request.path, user = get_user())
    else: #Posted back to page
        try:
            #get data from form
            user_name = request.form['user_name']
            display_name = request.form['display_name']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            #create insance of User
            new_user = User(-1, user_name, display_name, password)
            #check for miss matched password
            if (password != confirm_password):
                errors = new_user.get_errors
                errors.append ("Passwords do not match.")
                raise ExceptionList(errors)
            #matched passwords-> hashed password to new_user
            new_user.password = generate_password_hash(password)

            #add to DB
            Database.add_user(new_user)
        except ExceptionList as e:
            return render_template("users.html", users = users, errors = e.error_list,
                    return_url=request.path, user = get_user())
        # except: # catch all other exceptions
        #     abort(500)
        
        #reload page after user added
        return render_template("users.html", users = users,
                                return_url=request.path, user = get_user())
                        

# ADD USER                  ACTION METHOD
@controller.route("/users/add_user", methods =["POST",])
@admin_permission_required
def add_user():
    print("st: add_user")

    try:
        #get data from form
        user_name = request.form['user_name']
        display_name = request.form['display_name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']


        #create insance of User
        new_user = User(-1, user_name, display_name, password)
        
        if (password != confirm_password):
            errors = new_user.get_errors
            errors.append ("Passwords do not match.")
            raise ExceptionList(errors)
        
     

        #add to DB
        Database.add_user(new_user)

    except ExceptionList:
        abort(404)
    except sqlite3.Error as e:
        abort(500)
    except Exception as e:
        abort(500)
    return redirect("/users")


# DELETE USER CONFIRMATION      VIEW METHOD
@controller.route("/users/confirm_delete_user", methods = ['POST'])
@admin_permission_required
def confirm_delete_user():
    try:
        user_id = int(request.form['user_id'])

        target_user = Database.get_user(user_id)
        if not target_user:
            abort(500)

    except ExceptionList:
        abort(404)
    except Exception:
        abort(500)
    return render_template("confirm_delete_user.html", user = target_user)



# DELETE USER                      ACTION METHOD
@controller.route("/users/delete_user", methods = ['POST'])
@admin_permission_required
def delete_user():
    try:
        user_id = int(request.form['user_id'])

        target_user = Database.get_user(user_id)
        if not target_user:
            abort(500)
        Database.delete_user(user_id)


    except ExceptionList:
        abort(404)
    # except Exception:
    #     abort(500)
    return redirect("/users")