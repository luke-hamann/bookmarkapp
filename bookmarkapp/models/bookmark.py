"""
    Title: Bookmark Class
    Properties: id, title, url, blurb, description
    Methods: get_errors
    Description: Represents bookmarks w/ properties.
                 Has function to validate properties meet desired criteria
"""

class Bookmark:
    #static variables
    _TITLE_MAX_LENGTH = 70
    _URL_MAX_LENGTH = 1_000
    _BLURB_MAX_LENGTH = 100
    _DESCRIPTION_MAX_LENGTH = 1_000_000


    #Constructor for Bookmark
    def __init__(self, id: int = 1, title: str = '', url: str = '', blurb: str = '', description: str = '') -> None:
        self.id = id
        self.title = title
        self.url = url
        self.blurb = blurb
        self.description = description

    def get_errors(self) -> list[str]:
        #returns a list of errors based on invalid values of properties
        errors = []

        # Validate title
        if (self.title == ''):
            errors.append("Bookmark title is required.")
        else:
            if (len(self.title) > Bookmark._TITLE_MAX_LENGTH):
                errors.append(f"Bookmark title must be {Bookmark._TITLE_MAX_LENGTH:,} characters or less.")
            if ("\n" in self.title):
                errors.append("Bookmark title must not contain new line characters.")
        
        # Validate URL
        if (self.url == ''):
            errors.append("Bookmark URL is required.")
        else:
            tests_passed = [
                ("." in self.url),
                ("\n" not in self.url),
                (self.url.startswith("http://") or
                 self.url.startswith("https://"))
            ]

            if (not all(tests_passed)):
                errors.append("Bookmark URL must be a well-formed URL.")
            if (len(self.url) > Bookmark._URL_MAX_LENGTH):
                errors.append(f"Bookmark URL must be {Bookmark._URL_MAX_LENGTH:,} characters or less.")

        # Validate blurb
        if (len(self.blurb) > Bookmark._BLURB_MAX_LENGTH):
            errors.append(f"Bookmark blurb must be {Bookmark._BLURB_MAX_LENGTH:,} characters or less.")
        if ("\n" in self.blurb):
            errors.append("Bookmark blurb must not contain new line characters.")

        # Validate description
        if (len(self.description) > Bookmark._DESCRIPTION_MAX_LENGTH):
            errors.append(f"Bookmark description must be {Bookmark._DESCRIPTION_MAX_LENGTH:,} characters or less.")
        
        return errors
