"""
    Title: User Class
    Properties: id, username, display_name, password, privilege
    Methods: get_errors
"""
import re
from bookmarkapp.models.util import is_user_name_unique, is_display_name_unique


class User:
    _USER_NAME_MAX_LENGTH = 30
    _USER_NAME_MIN_LENGTH = 4

    _DISPLAY_NAME_MAX_LENGTH = 30
    _DISPLAY_NAME_MIN_LENGTH = 4

    _PASSWORD_MAX_LENGTH = 64
    _PASSWORD_MIN_LENGTH = 8

    

    def __init__(self, id: int = -1, user_name: str = ''  , display_name: str = '', password: str = '', privilege: str = 'user') -> None:
        self.id = id
        self.user_name = user_name
        self.display_name = display_name
        self.password = password
        self.privilege = privilege


    def get_errors(self) -> list[str]:
        #Checks critera for validation of all properties of  User &
        #returns a list w/ each conflict 
        errors = []
        temp_errors_count = 0
        
        # Validate username
        if (self.user_name == ''):
            errors.append("Username is required.")
        if (len(self.user_name ) > User._USER_NAME_MAX_LENGTH or (len(self.user_name ) < User._USER_NAME_MIN_LENGTH)):
            errors.append(f"Username name must be between {User._USER_NAME_MIN_LENGTH} and {User._USER_NAME_MAX_LENGTH:,} characters long.")
        pattern = r'[^a-zA-Z0-9_]'
        if (re.search(pattern, self.user_name)):
            errors.append("Usernames can only contain letters (a-z, A-Z), numbers (0-9) and underscores(_).")
        # If no errors w/ username, check if username is taken
        if (len(errors) == 0):
            if not (is_user_name_unique(self.user_name)):
                errors.append("Username is in use. Please enter a different username")
        #store count to compare after display_name validation
        temp_errors_count = len(errors)


        # Validate display name
        if (self.display_name == ''):
            errors.append("Display name is required.")
        if (len(self.display_name ) > User._DISPLAY_NAME_MAX_LENGTH) or (len(self.display_name ) < User._DISPLAY_NAME_MIN_LENGTH):
            errors.append(f"Display name must be between {User._DISPLAY_NAME_MIN_LENGTH} and {User._DISPLAY_NAME_MAX_LENGTH:,} characters long.")
        pattern = r'[^a-zA-Z0-9_]'
        if (re.search(pattern, self.display_name)):
            errors.append("Display name can only contain letters (a-z, A-Z), numbers (0-9) and underscores(_).")

        # If no errors w/ display_name, check if display name is taken
        if (len(errors) == temp_errors_count):
            if not (is_display_name_unique(self.display_name)):
                errors.append("Display name is in use. Please enter a different display name")

        # Validate password
        if (self.password == ''):
            errors.append("Password  is required.")
        if (len(self.password) > User._PASSWORD_MAX_LENGTH) or (len(self.password) < User._PASSWORD_MIN_LENGTH):
                errors.append(f"Password must be between {User._PASSWORD_MIN_LENGTH:,}-{User._PASSWORD_MAX_LENGTH:,} characters long.")
        
        
            # reg ex pattern to check for 1 number 0-9 & 1 special character, only a-z,A-Z,0-9,!@#$%^&*()
        pattern = r'^(?=.*[0-9])(?=.*[!@#$%^&*()])[0-9A-Za-z!@#$%^&*()]+$'
        if (not re.match(pattern, self.password)):
            errors.append("Password must contain at least 1 number(0-9), and 1 special character(e.g. $, %, &, #, etc).")
    

    
        # Validate privilege
        if (self.privilege not in ['admin', 'user']):
            errors.append("Privilege type must be an approved value.")


        #Return list of errors
        return errors