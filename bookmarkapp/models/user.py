"""
    Title: User Class
    Authors: Malachi Harris & Luke Hamann
    Date: 2024-08-31
    Updated: 2024-09-13
    Purpose: This file provides a data class for representing users.
    Properties: id, username, display_name
    Methods: None
"""

class User:
    def __init__(self, id: int = 1, username: str = '', display_name: str = '') -> None:
        self.id = id
        self.username = username
        self.display_name = display_name
