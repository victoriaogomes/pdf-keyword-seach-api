class NoPdfFoundException(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code
        super().__init__(message)