from starlette.datastructures import UploadFile
class CorrectParserNotFound(Exception):
    
    def __init__(self, file: UploadFile | str) -> None:
        if type(file) is str:
            self.message = f"The Parser for this file ({file}) type was not found"
        elif type(file) is UploadFile:
            self.message = f"The Parser for this file ({file.filename}) type was not found"
        else:
            self.message = f"The Parser for this file type was not found"

        super().__init__(self.message)