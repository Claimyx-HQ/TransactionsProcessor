
from typing import List


class ParserMismatchException(Exception):
    def __init__(self, parsers: List|None = None, message: str = None):
        if parsers is not None:
            self.parsers = parsers
            try:
                parser_names = [self.parsers[i].__name__ for i in range(len(self.parsers))]
                message = f"Bank files have differing parsers: {', '.join(set(parser_names))}"
            except: 
                # if the parsers are strings
                message = f"Bank files have differing parsers: {', '.join(set(self.parsers))}"
        else:
            if message is None:
                message = "The parser for this file type was not found"
        super().__init__(message)
