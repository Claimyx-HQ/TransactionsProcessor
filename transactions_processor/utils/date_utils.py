from datetime import datetime

def valid_date(date: str | float, format: str = "%m/%d/%Y") -> bool:
    try:
        if isinstance(date, float):
            return False
        datetime.strptime(date, format)
        return True
    except ValueError:
        return False


def valid_date_split(date: str | float, split_str: str) -> bool:
    try:
        if isinstance(date, float):
            return False
        datetime.strptime(date.split(split_str)[0], "%m/%d/%Y")
        return True
    except ValueError:
        return False
