import re
import math

def valid_amount(amount: float) -> bool:
    return not (math.isnan(amount) or amount <= 0.0)

def parse_amount(amount_string: str | float) -> float:
    amount = (
        float(re.sub(r'[^\d.]', '', amount_string))
        if isinstance(amount_string, str)
        else float(amount_string)
    )
    return amount
