"""
    Title: Exception List Class
    Purpose: Provide an exception type that allows for multiple messages
    Properties: error_list
    Methods: None
"""

class ExceptionList(Exception):
    #Exception that handles a list of strings.
    #Used for delivoring validation messages to user for input forms
    def __init__(self, error_list: list[str] = []) -> None:
        self.error_list = error_list
