from pathlib import PurePath
import sqlite3
from bookmarkapp.models.bookmark import Bookmark
from bookmarkapp.models.exceptionlist import ExceptionList
from bookmarkapp.models.user import User

class Database:
    _DATABASE_FILE = PurePath('bookmarkapp', 'data', 'database.db')

    def _get_cursor() -> sqlite3.Cursor:
        connection = sqlite3.connect(Database._DATABASE_FILE)
        cursor = connection.cursor()
        return cursor
    
    def get_all_bookmarks() -> list[Bookmark]:
        try:
            result = Database._get_cursor().execute("""
                SELECT id, title, url, blurb, description
                FROM bookmarks
                ORDER BY LOWER(title);
            """)
            rows = result.fetchall()
        except:
            raise ExceptionList(["There was an error connecting to the database."])
        
        bookmarks = []
        for row in rows:
            [id, title, url, blurb, description] = row
            bookmark = Bookmark(id, title, url, blurb, description)
            bookmarks.append(bookmark)
        return bookmarks

    def get_bookmark(id: int) -> Bookmark:
        try:
            result = Database._get_cursor().execute("""
                SELECT title, url, blurb, description
                FROM bookmarks
                WHERE id = ?;
            """, (id, ))
            row = result.fetchone()
        except:
            raise ExceptionList(["There was an error connecting to the database."])
        
        if (row is None):
            return None
        
        [title, url, blurb, description] = row
        return Bookmark(id, title, url, blurb, description)

    def add_bookmark(bookmark: Bookmark, user: User) -> Bookmark:
        if (user is None):
            raise ExceptionList(["Authentication is required to add a bookmark."])
        
        bookmark_errors = bookmark.get_errors()
        if (len(bookmark_errors) > 0):
            raise ExceptionList(bookmark_errors)
        
        try:
            cursor = Database._get_cursor()
            cursor.execute("""
                INSERT INTO bookmarks (title, url, blurb, description)
                VALUES (?, ?, ?, ?);
            """, (bookmark.title, bookmark.url, bookmark.blurb, bookmark.description))
            cursor.connection.commit()
            id = cursor.lastrowid
        except:
            raise ExceptionList(["There was an error connecting to the database."])
        
        bookmark.id = id
        return bookmark

    def update_bookmark(bookmark: Bookmark, user: User) -> None:
        if (user is None):
            raise ExceptionList(["Authentication is required to update a bookmark."])
        
        bookmark_errors = bookmark.get_errors()
        if (len(bookmark_errors) > 0):
            raise ExceptionList(bookmark_errors)
        
        try:
            cursor = Database._get_cursor()
            cursor.execute("""
                UPDATE bookmarks
                SET title = ?,
                    url = ?,
                    blurb = ?,
                    description = ?
                WHERE id = ?;
            """, (bookmark.title, bookmark.url, bookmark.blurb, bookmark.description, bookmark.id))
            cursor.connection.commit()
            if (cursor.rowcount == 0):
                raise ExceptionList(["That bookmark does not exist."])
        except ExceptionList as ex:
            raise ex
        except:
            raise ExceptionList(["There was an error connecting to the database."])

    def delete_bookmark(bookmark: Bookmark, user: User) -> None:
        if (user is None):
            raise ExceptionList(["Authentication is required to delete a bookmark."])

        try:
            cursor = Database._get_cursor()
            cursor.execute("""
                DELETE FROM bookmarks
                WHERE id = ?;
            """, (bookmark.id, ))
            cursor.connection.commit()
            if (cursor.rowcount == 0):
                raise ExceptionList(["That bookmark does not exist."])
        except ExceptionList as ex:
            raise ex
        except:
            raise ExceptionList(["There was an error connecting to the database."])

    def get_user(id: int) -> User:
        if (id == 1):
            return User(1, 'admin', 'Administrator')
        else:
            raise ExceptionList(["That user does not exist."])

    def authenticate_user(username: str, password: str) -> User:
        errors = []
        if (username == ''):
            errors.append('Username is required.')
        if (password == ''):
            errors.append('Password is required.')

        if (len(errors) > 0):
            raise ExceptionList(errors)

        if ((username == 'admin') and (password == 'password')):
            return User(1, 'admin', 'Administrator')
        else:
            raise ExceptionList(["Invalid credentials."])
