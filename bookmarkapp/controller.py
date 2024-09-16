"""
    Title: Application Controller
    Authors: Malachi Harris & Luke Hamann
    Date: 2024-08-31
    Updated: 2024-09-13
    Purpose: Create a Flask blueprint to serve as the controller
"""

from functools import wraps
from flask import abort, Blueprint, redirect, render_template, request, url_for
from bookmarkapp.models import Bookmark, Database, ExceptionList, User
from bookmarkapp.models.user_checks import is_user_name_unique, is_display_name_unique
import sqlite3
from bookmarkapp.models import Database
from bookmarkapp.auth import get_user, set_user, get_csrf_token

controller = Blueprint('controller', __name__, url_prefix='/')

# Helper functions

def get_bookmark_from_form() -> Bookmark:
    #gets vars from POST & uses them to return a Bookmark
    title = request.form.get('title', '').strip()
    url = request.form.get('url', '').strip()
    blurb = request.form.get('blurb', '').strip()
    description = request.form.get('description', '')
    return Bookmark(1, title, url, blurb, description)

def validate_return_url(return_url):
    #ensures url either starts w/ '/' or doesn't start w/ '//', if it does => url ='/'
    if (return_url.startswith("//") or not return_url.startswith("/")):
        return_url = "/"
    return return_url


# View wrappers
# LOGIN_REQUIRED                WRAPPER FUNCTION
def login_required(old_function):
    #validates the client has a valid user in the session else: redirects to login
    @wraps(old_function)
    def new_function(*args, **kwargs):
        if (get_user() is None):
            return redirect(f"/login?return_url={request.path}")
        return old_function(*args, **kwargs)
    return new_function

# ADMIN_PERMISSION_REQUIRED     WRAPPER FUNCTION
def admin_permission_required(old_function):
    #validates the client has a user w/ admin privilege in the session else: redirects to login
    @wraps(old_function)
    def new_function(*args, **kwargs):
        if (get_user().privilege != 'admin'):
            abort(403)
        return old_function(*args, **kwargs)
    
    return new_function
# CSRF PROTECTED                WRAPPER FUNCTION
def csrf_protected(old_function):
    #On pages enterd by POST request, 
    #Compares csrf_token in POST to csrf_token in SESSION, if != then  abort(401)
    @wraps(old_function)
    def new_function(*args, **kwargs):
        if ((request.method == "POST") and
            (request.form.get('csrf_token', None) != get_csrf_token())):
            abort(401)
        return old_function(*args, **kwargs)
    return new_function



# ----------------------------------------------    Bookmark funcitons     ----------------------------------------------


# ------------- Bookmark Read Only -----------------

#BOOKMARK LIST PAGE         VIEW FUNCTION
@controller.route("/", methods=['GET'])
def index():
    try:
        bookmarks = Database.get_all_bookmarks()
    except:
        abort(500)

    return render_template("index.html", 
                           bookmarks=bookmarks, 
                           user=get_user(),
                           return_url="/", 
                           csrf_token=get_csrf_token())


#DETAIL<id> PAGE            VIEW FUNCTION
@controller.route("/<int:id>", methods=['GET'])
def detail(id):
    try:
        bookmark = Database.get_bookmark(id)
    except ExceptionList:
        abort(404)
    except:
        abort(500)

    return render_template("detail.html", 
                           bookmark=bookmark, 
                           return_url=request.path, 
                           user=get_user(), 
                           csrf_token=get_csrf_token())

# Form Views
# ------------- Bookmark CRUD  -----------------

#ADD BOOKMARK PAGE              VIEW FUNCTION
@controller.route("/add", methods=["GET", "POST"])
@login_required
@csrf_protected
def add():
    #page w/ form for user to add bookmark

    
    if (request.method == "GET"):
        #initial entry: load add.html
        return render_template('add.html', 
                               bookmark=None, 
                               user=get_user(),
                               return_url=request.path,
                               csrf_token=get_csrf_token())
    else:
        try:
            #on post, try to make bookmark & add to DB
            bookmark = get_bookmark_from_form()
            id = Database.add_bookmark(bookmark, get_user())
        except ExceptionList as e:
            #on failed atttempt, reload page w/ error_list
            return render_template('add.html', 
                                   bookmark=bookmark,
                                   errors=e.error_list, 
                                   user=get_user(),
                                   return_url=request.path,
                                   csrf_token=get_csrf_token())

        #on success redirect to newly created bookmark detail page
        return redirect(id)


#DETAIL<id> EDIT PAGE           VIEW FUNCTION
@controller.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
@csrf_protected
def edit(id):
    if (request.method == "GET"):
        try:
            bookmark = Database.get_bookmark(id)
        except ExceptionList:
            abort(404)
        except:
            abort(500)

        return render_template('edit.html', 
                               bookmark=bookmark, 
                               user=get_user(), 
                               csrf_token=get_csrf_token())
    else:
        bookmark = get_bookmark_from_form()
        bookmark.id = id

        try:
            Database.update_bookmark(bookmark, get_user())
        except ExceptionList as e:
            return render_template('edit.html', 
                                   bookmark=bookmark,
                                   errors=e.error_list, 
                                   user=get_user(),
                                   csrf_token=get_csrf_token())
        return redirect(f'/{id}')

#DETAIL DELETE ROUTE            ACTION FUNCTION
@controller.route("/<int:id>/delete", methods=["GET", "POST"])
@login_required
@csrf_protected
def delete(id):
    try:
        bookmark = Database.get_bookmark(id)
    except ExceptionList:
        abort(404)
    except:
        abort(500)

    if (request.method == 'GET'):
        return render_template('delete.html', 
                               bookmark=bookmark,
                               user=get_user(),
                               csrf_token=get_csrf_token())
    else:
        try:
            Database.delete_bookmark(bookmark, get_user())
        except ExceptionList as e:
            return render_template('delete.html', 
                                   bookmark=bookmark,
                                   user=get_user(),
                                   csrf_token=get_csrf_token())

        return redirect('/')

# ----------------------------------------------    Authentication     ----------------------------------------------

#LOGIN PAGE                 VIEW FUNCTION
@controller.route("/login", methods=["GET", "POST"])
@csrf_protected
def login():
    if (request.method == 'GET'):
        return_url = request.args.get('return_url', '/')
        return_url = validate_return_url(return_url)

        #If no user load, else send back
        if (get_user() is None):
            return render_template("login.html", 
                                   return_url=return_url,
                                   csrf_token=get_csrf_token())
        else:
            return redirect(return_url)
        

    else:   #On POST
        #get data from post
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        return_url = request.form.get('return_url', '/')
        return_url = validate_return_url(return_url)

        #try to authenticate, else reload w/ errors
        try:
            user = Database.authenticate_user(username, password)

        except ExceptionList as e:
            return render_template("login.html", 
                                   errors=e.error_list,
                                   return_url=return_url, 
                                   username=username,
                                   csrf_token=get_csrf_token())

        set_user(user)
        return redirect(return_url)

#LOGOUT ROUTE               ACTION FUNCTION
@controller.route("/logout", methods=["GET", "POST"])
@csrf_protected
def logout():
    if (request.method == 'POST'):
        set_user(None)
    return redirect(url_for('controller.index'))

# ----------------------------------------------    User Functionalty    ----------------------------------------------
# USERS LIST                VIEW FUNCTION
@controller.route("/users", methods=["GET"])
@admin_permission_required
@csrf_protected
def users():
    #page to allow admin to see user accounts and delete or add them

    #access DB to get user data for table
    try:
        users = Database.get_all_users_for_table()
    except ExceptionList:
        abort(404)
    except:
        abort(500)

    
    return render_template("users.html", 
                            users = users,
                            return_url=request.path, 
                            user = get_user(),
                            csrf_token=get_csrf_token())




# DELETE USER CONFIRMATION      VIEW FUNCTION
@controller.route("/users/confirm_delete_user", methods = ['POST'])
@admin_permission_required
@csrf_protected
def confirm_delete_user():
    try:
        #get id from POST => User from DB
        user_id = int(request.form['user_id'])
        target_user = Database.get_user(user_id)

        #if no user in DB => abort
        if (not target_user):
            abort(404)
        
        # if target is admin => abort
        if (target_user.privilege == 'admin'):
            abort(403)
        
        #render confirm_delete_user
        return render_template("confirm_delete_user.html", 
                               user = get_user(),
                               target_user = target_user, 
                               csrf_token=get_csrf_token())

    except ExceptionList:
        abort(404)
    except Exception:
        abort(500)
   



# DELETE USER                      ACTION FUNCTION
@controller.route("/users/delete_user", methods = ['POST'])
@admin_permission_required
@csrf_protected
def delete_user():
    try:
        #get id from POST => User from DB
        user_id = int(request.form['user_id'])
        target_user = Database.get_user(user_id)

        # if target is admin => abort
        if (target_user.privilege == 'admin'):
            abort(403)

        #if no user in DB => abort
        if not target_user:
            abort(500)
        Database.delete_user(user_id, get_user())


    except ExceptionList:
        abort(404)
    except Exception:
        abort(500)
    return redirect("/users")


# ADD USER                          VIEW FUNCTION
@controller.route("/users/add", methods = ['GET', 'POST'])
@admin_permission_required
@csrf_protected
def add_user():
    #page w/ form for admin to add user
    if (request.method == "GET"):
        #initial entry: load add.html
        return render_template('add_user.html', 
                               new_user=None, 
                               user=get_user(),
                               return_url=request.path,
                               csrf_token=get_csrf_token())
    else: #Posted back to page
            try:
                #get data from form
                user_name = request.form['user_name']
                display_name = request.form['display_name']
                password = request.form['password']
                confirm_password = request.form['confirm_password']


                #create insance of User
                new_user = User(-1, user_name, display_name, password)
                #check for non-matching passwords
                if (password != confirm_password):
                    errors = new_user.get_errors()
                    errors.append ("Passwords do not match.")
                    raise ExceptionList(errors)

                #if errors, raise exception
                errors = new_user.get_errors()
                if (len(errors) > 0):
                    raise ExceptionList(errors)


                #add to DB
                Database.add_user(new_user, auth_user= get_user())

            except ExceptionList as e:
                return render_template("add_user.html", 
                                    new_user = new_user, 
                                    errors = e.error_list,
                                    return_url=request.path, 
                                    user = get_user(),
                                    csrf_token=get_csrf_token())
            except: # catch all other exceptions
                abort(500)
            
            # On success, redirect to /users
            return redirect("/users")
        

