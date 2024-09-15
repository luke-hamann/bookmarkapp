"""
    Title: Authentication Helper Fuctions
    Purpose: Provide an interface for accessing a user and a CSRF token in a
             Flask session
"""

from secrets import token_hex
from flask import session
from bookmarkapp.models import User, Database

def get_user() -> User:
    #returns a user based on value of userId in session
    userId = session.get('userId', None)
    if (userId is None):
        return None
    else:
        return Database.get_user(userId)

def set_user(user: User) -> None:
    #sets userId in session base on User in argument
    if (user is None):
        session['userId'] = None
    else:
        session['userId'] = user.id

def get_csrf_token() -> str:
    if (session.get('csrf_token', None) is None):
        session['csrf_token'] = token_hex(256)
    return session['csrf_token']
