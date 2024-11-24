# One to one matching
from typing import Dict, List, Tuple
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


class ExcludedGroup(BaseModel):
    key: str
    values: List[str]


class ExcludedDescriptions(BaseModel):
    bank: List[ExcludedGroup]
    system: List[ExcludedGroup]
