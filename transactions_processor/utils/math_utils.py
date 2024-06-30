import re
import math


def valid_amount(amount: float) -> bool:
    return not (math.isnan(amount) or amount <= 0.0)


def parse_amount(amount_string: str | float) -> float:
    if isinstance(amount_string, float):
        return amount_string
    elif isinstance(amount_string, int):
        return float(amount_string)
    is_negative = (
        len(amount_string) >= 2 and amount_string[0] == "(" and amount_string[-1] == ")"
    )
    amount = float(re.sub(r"[^\d.]", "", amount_string)) * (-1 if is_negative else 1)
    return amount
