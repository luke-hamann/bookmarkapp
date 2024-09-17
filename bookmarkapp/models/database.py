"""
    Title: Database Class
    Authors: Malachi Harris & Luke Hamann
    Date: 2024-08-31
    Updated: 2024-09-17
    Purpose: This file provides a data class for accessing the database.
             It has various methods that allow CRUD interactions w/ both the Bookmarks and Users tables.
    Properties: None
    Methods: get_all_bookmarks, get_bookmark, add_bookmark, update_bookmark,
             delete_bookmark, get_user, authenticate_user,
             get_all_users_for_table, add_user, delete_user
"""

import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from bookmarkapp.models import Bookmark, ExceptionList, User

class Database:
    _DATABASE_PATH = 'bookmarkapp/data/database.db'

    @classmethod
    def _get_cursor(cls) -> sqlite3.Cursor:
        #return cursor to interact w/ database
        return sqlite3.connect(cls._DATABASE_PATH).cursor()

    @classmethod
    def get_all_bookmarks(cls) -> list[Bookmark]: 
        #executes query and then returns a list w/ Bookmark objects made from result
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
        #Performs query to return a single bookmark based on ID parameter
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
        #After validation, Inserts a bookmark into the database
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
        #After Validation, updates bookmark in the database
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
        #After validation, deletes bookmark from database
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
        #Gets user from database
        if id > -1:
            cursor = cls._get_cursor()
            cursor.execute(
                """
                SELECT id, display_name, privilege
                FROM users
                WHERE id = ?
                """, (id,))
            row = cursor.fetchone()
            #no user, raise exception
            if row is None:
                raise ExceptionList(["User not found"])  
            #make user with minimal data
            try:
                user = User(row[0], "", row[1], "", row[2])
            except Exception as e:
                raise ExceptionList(["Unable to create User"]) 
            #return user 
            return user
        else:
            raise ExceptionList(['That user does not exist.']) 



    @classmethod
    def authenticate_user(cls, user_name: str, password: str) -> User:
        #Authenticates users login attempt
        errors = []
        if (user_name == ''):
            errors.append('Username is required.')
        if (password == ''):
            errors.append('Password is required.')

        cursor = cls._get_cursor()
        cursor.execute("""
                        SELECT id, user_name, display_name, password, privilege
                        FROM users
                        WHERE user_name = ?
                        """, (user_name,))
        row = cursor.fetchone()

        #no username match in DB, raise error
        if (not row):
            errors.append('Invalid username or password.')
            raise ExceptionList(errors)
        
            
        #check if password entered matches password in users
        if (row[3] and password):
            if not (check_password_hash(row[3], password)):
                errors.append('Invalid username or password.')

        #raise exception if any errors
        if (len(errors) > 0):
            raise ExceptionList(errors)


        #client has enter validated username & password
        #return  User object w/ ID, display name, & privilege
        return User(*row)




    @classmethod
    def get_all_users_for_table(cls) -> list[User]:
        #Queries for all users from database, returned as a list of User objects
        try: 
            cursor = cls._get_cursor()
            cursor.execute("""
                            SELECT id, user_name, display_name, privilege
	                        FROM users
	                        ORDER BY LOWER(privilege), LOWER(user_name);
                           """)
            rows = cursor.fetchall()
        except sqlite3.Error as e:

            raise ExceptionList([f'Database error occured: {str(e)}'])
        finally:
            cursor.connection.close()

        users = []
        for row in rows:
            users.append(User(row[0], row[1], row[2], "", row[3] ))
        return users



    @classmethod
    def add_user(cls, user: User, auth_user: User):
        #After authentication, Inserts user into database
        if (auth_user.privilege != 'admin'):
            raise ExceptionList(['Authentication is required to add a user.'])

        errors = user.get_errors()
        if (len(errors) > 0):
            raise ExceptionList(errors)

        #hash password of new_user
        user.password = generate_password_hash(user.password)
        try: 
            cursor = cls._get_cursor()
            cursor.execute("""
                            INSERT INTO users
                            (user_name, display_name, password, privilege)
                            VALUES
                            (?, ?, ?, ?)
                           """, (user.user_name, user.display_name, user.password, user.privilege))
            cursor.connection.commit()

        except sqlite3.Error as e:
            raise ExceptionList([f'Database error occured: {str(e)}'])
        finally:
            cursor.connection.close()
        
    
    @classmethod
    def delete_user(cls, user_id, auth_user: User):
        #After authentication, deletes user from database
        if (auth_user.privilege != 'admin'):
            raise ExceptionList(['Authentication is required to delete a user.'])

        try: 
            cursor = cls._get_cursor()
            cursor.execute("""
                            DELETE FROM users
                            WHERE id = ?
                           """, (user_id,))
            cursor.connection.commit()

        except sqlite3.Error as e:
            raise ExceptionList([f'Database error occured: {str(e)}'])
        finally:
            cursor.connection.close()