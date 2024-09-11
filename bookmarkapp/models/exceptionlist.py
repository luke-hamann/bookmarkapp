"""
    Title: Exception List Class
    Purpose: Provide an exception type that allows for multiple messages
    Properties: error_list
    Methods: None
"""

class ExceptionList(Exception):
    def __init__(self, error_list: list[str] = []) -> None:
        self.error_list = error_list
