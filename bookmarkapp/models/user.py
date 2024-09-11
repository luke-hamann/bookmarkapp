"""
    Title: User Class
    Properties: id, username, display_name
    Methods: None
"""

class User:
    def __init__(self, id: int = 1, username: str = '', display_name: str = '') -> None:
        self.id = id
        self.username = username
        self.display_name = display_name
