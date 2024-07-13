class UnreadableFileException(Exception):
    def __init__(self, message):
        super().__init__(f"File could not be read: {message}")
