from transactions_processor.services.parsers.csv_parser import CSVParser


class NCSParser(CSVParser):
    def __init__(self) -> None:
        super().__init__(0, 3, 1, 6)
