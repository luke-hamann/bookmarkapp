"""
    Title: Database Class
    Authors: Malachi Harris & Luke Hamann
    Date: 2024-08-31
    Updated: 2024-09-13
    Purpose: This file provides a data class for accessing the database.
    Properties: None
    Methods: get_all_bookmarks, get_bookmark, add_bookmark, update_bookmark,
             delete_bookmark, get_user, authenticate_user
"""

import sqlite3
from bookmarkapp.models import Bookmark, ExceptionList, User

class Database:
    _DATABASE_PATH = 'bookmarkapp/data/database.db'

    @classmethod
    def _get_cursor(cls) -> sqlite3.Cursor:
        return sqlite3.connect(cls._DATABASE_PATH).cursor()

    @classmethod
    def get_all_bookmarks(cls) -> list[Bookmark]:
        try:
            cursor = cls._get_cursor()
            cursor.execute("""
                           SELECT id, title, url, blurb, description
                           FROM bookmarks
                           ORDER BY LOWER(title);
                           """)
            rows = cursor.fetchall()
        except sqlite3.Error as e:
            raise ExceptionList([f'Database error occured: {str(e)}'])
        finally:
            cursor.connection.close()

        bookmarks = []
        for row in rows:
            bookmarks.append(Bookmark(*row))
        return bookmarks

    @classmethod
    def get_bookmark(cls, id: int) -> Bookmark: 
        try:
            cursor = cls._get_cursor()
            cursor.execute("""
                           SELECT id, title, url, blurb, description
                           FROM bookmarks
                           WHERE id = ?;
                           """, (id, ))
            row = cursor.fetchone()
        except sqlite3.Error as e:
            raise ExceptionList([f'Database error occured: {str(e)}'])
        finally:
            cursor.connection.close()
        
        if (row is None):
            raise ExceptionList(['That bookmark does not exist.'])
        
        return Bookmark(*row)
    
    @classmethod
    def add_bookmark(cls, bookmark: Bookmark, user: User) -> int:
        if (user is None):
            raise ExceptionList(['Authentication is required to add a bookmark.'])

        errors = bookmark.get_errors()
        if (len(errors) > 0):
            raise ExceptionList(errors)

        try:
            cursor = cls._get_cursor()
            b = bookmark
            cursor.execute("""
                           INSERT INTO bookmarks (title, url, blurb, description)
                           VALUES (?, ?, ?, ?);
                           """, (b.title, b.url, b.blurb, b.description))
            id = cursor.lastrowid
            cursor.connection.commit()
        except sqlite3.Error as e:
            raise ExceptionList([f'Database error occured: {str(e)}'])
        finally:
            cursor.connection.close()

        return id

    @classmethod
    def update_bookmark(cls, bookmark: Bookmark, user: User) -> None:
        if (user is None):
            raise ExceptionList(['Authentication is required to update a bookmark.'])

        errors = bookmark.get_errors()
        if (len(errors) > 0):
            raise ExceptionList(errors)

        try:
            cursor = cls._get_cursor()
            b = bookmark
            cursor.execute("""
                           UPDATE bookmarks
                           SET title = ?, url = ?, blurb = ?, description = ?
                           WHERE id = ?;
                           """, (b.title, b.url, b.blurb, b.description, b.id))
            row_count = cursor.rowcount
            cursor.connection.commit()
        except sqlite3.Error as e:
            raise ExceptionList([f'Database error occured: {str(e)}'])
        finally:
            cursor.connection.close()

        if (row_count == 0):
            raise ExceptionList(['That bookmark does not exist.'])

    @classmethod
    def delete_bookmark(cls, bookmark: Bookmark, user: User) -> None:
        if (user is None):
            raise ExceptionList(['Authentication is required to delete a bookmark.'])

        try:
            cursor = cls._get_cursor()
            cursor.execute("""
                           DELETE FROM bookmarks
                           WHERE id = ?;
                           """, (bookmark.id, ))
            row_count = cursor.rowcount
            cursor.connection.commit()
        except sqlite3.Error as e:
            raise ExceptionList([f'Database error occured: {str(e)}'])
        finally:
            cursor.connection.close()

        if (row_count == 0):
            raise ExceptionList(['That bookmark does not exist.'])

    @classmethod
    def get_user(cls, id: int) -> User:
        if (id == 1):
            return User(1, 'a_user', 'Administrator')
        else:
            raise ExceptionList(['That user does not exist.'])

    @classmethod
    def authenticate_user(cls, username: str, password: str) -> User:
        errors = []
        if (username == ''):
            errors.append('Username is required.')
        if (password == ''):
            errors.append('Password is required.')

        if (len(errors) > 0):
            raise ExceptionList(errors)

        if ((username == 'a_user') and (password == 'pw2acct')) :
            return User(1, 'a_user', 'Administrator')
        else:
            raise ExceptionList(['Invalid credentials.'])
