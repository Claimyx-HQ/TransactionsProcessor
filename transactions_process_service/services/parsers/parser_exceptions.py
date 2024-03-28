
class CorrectParserNotFound(Exception):
    
    def __init__(self, file) -> None:
        self.message = f"The Parser for this file ({file.filename}) type was not found"
        super().__init__(self.message)