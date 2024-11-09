# One to one matching
from typing import List, Tuple
from pydantic import BaseModel

from transactions_processor.schemas.transaction import Transaction


class MatchedTransactions(BaseModel):
    matched: List[Tuple[Transaction, Transaction]]
    unmatched_bank: List[Transaction]
    unmatched_system: List[Transaction]


# Many to many matching
class ReconcilingMatches(BaseModel):
    matched: List[Tuple[List[Transaction], List[Transaction]]]  # Bank, System
    unmatched_bank: List[Transaction]
    unmatched_system: List[Transaction]
