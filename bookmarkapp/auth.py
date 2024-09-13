"""
    Title: Authentication Helper Fuctions
    Authors: Malachi Harris & Luke Hamann
    Date: 2024-09-05
    Updated: 2024-09-13
    Purpose: Provide an interface for accessing a user and a CSRF token in a
             Flask session
"""

from secrets import token_hex
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

def get_csrf_token() -> str:
    if (session.get('csrf_token', None) is None):
        session['csrf_token'] = token_hex(256)
    return session['csrf_token']
