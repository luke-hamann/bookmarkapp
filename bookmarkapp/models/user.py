"""
    Title: User Class
    Properties: id, username, display_name, password, privilege
    Methods: get_errors
"""
import re


class User:
    _USER_NAME_MAX_LENGTH = 30
    _USER_NAME_MIN_LENGTH = 4

    _DISPLAY_NAME_MAX_LENGTH = 30
    _DISPLAY_NAME_MIN_LENGTH = 4

    _PASSWORD_MAX_LENGTH = 64
    _PASSWORD_MIN_LENGTH = 8

    

    def __init__(self, id: int = -1, user_name: str = ''  , display_name: str = '', password: str = '', privilege: str = '') -> None:
        self.id = id
        self.user_name = user_name
        self.display_name = display_name
        self.password = password
        self.privilege = privilege


    def get_errors(self) -> list[str]:
        #Checks critera for validation of all properties of  User &
        #returns a list w/ each conflict 
        errors = []

        # Validate password
        if (self.password == ''):
            errors.append("Password  is required.")
        if (len(self.password) > User._password_MAX_LENGTH):
                errors.append(f"Password must be between {User._PASSWORD_MIN_LENGTH:,}-{User._PASSWORD_MAX_LENGTH:,} characters long.")
        if (len(self.password) < User._PASSWORD_MIN_LENGTH):
            errors.append(f"Password must be at least {User._PASSWORD_MAX_LENGTH:,} characters long.")
            # reg ex pattern to check for 1 number 0-9 & 1 special character
        pattern = r'^(?=.*[0-9])(?=.*[!@#$%^&*()]).+$'
        if (not re.match(pattern, self.password)):
            errors.append("Username must contain at least 1 number(0-9), and 1 special character(e.g. $, %, &, #, etc).")
    
        
        # Validate username
        if (self.user_name == ''):
            errors.append("Username is required.")
        if (len(self.user_name ) > _USER_NAME_MAX_LENGTH):
            errors.append(f"Username must be at least {User._USER_NAME_MAX_LENGTH:,} characters long.")
        if (len(self.user_name ) > _USER_NAME_MIN_LENGTH):
            errors.append(f"Username must be at least {User._USER_NAME_MIN_LENGTH:,} characters long.")
        pattern = r'[^a-zA-Z0-9]'
        if (re.search(pattern, self.user_name)):
            errors.append("Usernames can only contain letters (a-z, A-Z) and numbers (0-9).")
        

        # Validate display name
        if (self.display_name == ''):
            errors.append("Username is required.")
        if (len(self.display_name ) > _DISPLAY_NAME_MAX_LENGTH):
            errors.append(f"Username must be at least {User._DISPLAY_NAME_MAX_LENGTH:,} characters long.")
        if (len(self.display_name ) > _DISPLAY_NAME_MIN_LENGTH):
            errors.append(f"Username must be at least {User._DISPLAY_NAME_MIN_LENGTH:,} characters long.")
        pattern = r'[^a-zA-Z0-9]'
        if (re.search(pattern, self.display_name)):
            errors.append("Usernames can only contain letters (a-z, A-Z) and numbers (0-9).")


        # Validate privilege
        if (self.privilege not in ['admin', 'user']):
            errors.append("Privilege type must be an approved value. Contact site administrator for assistance.")

        return errors