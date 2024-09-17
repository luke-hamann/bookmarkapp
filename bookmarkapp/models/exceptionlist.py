"""
    Title: Exception List Class
    Authors: Malachi Harris & Luke Hamann
    Date: 2024-08-31
    Updated: 2024-09-13
    Purpose: Provide an exception type that allows for multiple messages
    Properties: error_list
    Methods: None
"""

class ExceptionList(Exception):
    #Exception that handles a list of strings.
    #Used for delivering validation messages to user for input forms
    def __init__(self, error_list: list[str] = []) -> None:
        self.error_list = error_list
