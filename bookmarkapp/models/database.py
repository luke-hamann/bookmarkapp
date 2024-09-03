import os
import sqlite3
from  .bookmark import Bookmark

class Database:
    path_to_db = os.path.dirname(__file__) + "/database.db"
    @classmethod
    def connect_to_db(cls):
        return sqlite3.connect(cls.path_to_db)

    @classmethod
    def get_all_bookmarks(cls) -> list[Bookmark]:
        bookmarks = []
        try:
            con = cls.connect_to_db()
            cursor = con.cursor()
            cursor.execute("SELECT * FROM bookmarks")
            rows = cursor.fetchall()
            for row in rows:
                new_bookmark = Bookmark(row[0],row[1],row[2],row[3],row[4])
                bookmarks.append(new_bookmark)
        except sqlite3.error as e:
            raise RuntimeError(f"Database error occured: {str(e)}")
        finally:
            con.close()
            return bookmarks

    @classmethod
    def get_bookmark(cls, id): 
        
        try:
            con = cls.connect_to_db()
            cursor = con.cursor()
            values = (id, )
            print(str(values))
            cursor.execute("SELECT * FROM bookmarks WHERE id = ?", values)
            row = cursor.fetchone()
            new_bookmark = Bookmark(row[0],row[1],row[2],row[3],row[4])
        except sqlite3.error as e:
            raise RuntimeError(f"Database error occured: {str(e)}")
        finally:
            con.close()
            return new_bookmark
    

    @classmethod
    def add_bookmark(cls, title, url, blurb, description):
        try:
            con = cls.connect_to_db()
            cursor = con.cursor()
            values = [title, url, blurb, description]
            cursor.execute("INSERT INTO bookmarks (title, url, blurb, description) VALUES(?, ?, ?, ?)", values)
            con.commit()
        except sqlite3.error as e:
            raise RuntimeError(f"Database error occured: {str(e)}")
        finally:
            con.close()
    @classmethod
    def update_bookmark(cls, id, title, url, blurb, description):
        try:
            con = cls.connect_to_db()
            cursor = con.cursor()
            values = [title, url, blurb, description, id]
            cursor.execute("UPDATE bookmarks SET title = ?, url = ?, blurb = ?, description = ? WHERE id = ?;", values)
            con.commit()
        except sqlite3.error as e:
            raise RuntimeError(f"Database error occured: {str(e)}")
        finally:
            con.close()

    @classmethod
    def delete_bookmark(cls, id):
        try:
            con = cls.connect_to_db()
            cursor = con.cursor()
            values = [id]
            cursor.execute("DELETE FROM bookmarks WHERE id = ?", values)
            con.commit()
        except sqlite3.error as e:
            raise RuntimeError(f"Database error occured: {str(e)}")
        finally:
            con.close()


    @classmethod
    def get_user(cls, id): 
        return  [1, "a_user", "pw2acct" ]


    @classmethod
    def authenticate_user(cls, username, password):
        is_member = False

        if (username == "a_user" and password == "pw2acct") :
            is_member = True

        return is_member