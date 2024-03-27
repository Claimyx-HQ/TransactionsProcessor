
from typing import List


class ParserMismatchException(Exception):
    def __init__(self, parsers: List[str]):
        self.parsers = parsers
        message = f"Bank files have differing parsers: {', '.join(set(parsers))}"
        super().__init__(message)
