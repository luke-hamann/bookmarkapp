"""
    Title: Util Class
    Properties: id, username, display_name, password, privilege
    Methods: get_errors
"""
import sqlite3
from bookmarkapp.models import ExceptionList




def _get_cursor() -> sqlite3.Cursor:
    _DATABASE_PATH = 'bookmarkapp/data/database.db'
    return sqlite3.connect(_DATABASE_PATH).cursor()

def is_user_name_unique(user_name) -> bool:
    #checks username argument against DB for any matches in user_name column
    cursor = None
    try:
        cursor = _get_cursor()
        cursor.execute("""
                        SELECT user_name
                        FROM users
                        WHERE user_name = ?
                        """, (user_name,))
        rows = cursor.fetchall()
    except sqlite3.Error as e:
        raise ExceptionList([f'Database error occured: {str(e)}'])
    finally:
        if not (cursor == None):
            cursor.connection.close()
    #if any rows, username is taken
    is_no_errors = (len(rows) == 0)
    return is_no_errors

def is_display_name_unique(display_name) -> bool:
    #checks display name argument against DB for any matches in display_name column
    cursor = None
    try:
        cursor = _get_cursor()
        cursor.execute("""
                        SELECT display_name
                        FROM users
                        WHERE display_name = ?
                        """, (display_name,))
        rows = cursor.fetchall()
    except sqlite3.Error as e:
        raise ExceptionList([f'Database error occured: {str(e)}'])
    finally:
        if not (cursor == None):
            cursor.connection.close()
    
    #if any rows, display name is taken
    is_no_errors = (len(rows) == 0)
    return is_no_errors