"""
    Title: Authentication Helper Fuctions
    Purpose: Provide an interface for saving and loading a user in a Flask session
"""

from flask import session
from bookmarkapp.models import User, Database

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
