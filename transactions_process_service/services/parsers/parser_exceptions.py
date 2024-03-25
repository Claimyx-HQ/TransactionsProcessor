
class CorrectParserNotFound(Exception):
    
    def __init__(self, message: str = "The Parser for this file type was not found") -> None:
        self.message = message
        super().__init__(self.message)