class ExceptionList(Exception):
    def __init__(self, error_list: list[str] = []):
        self.error_list = error_list
