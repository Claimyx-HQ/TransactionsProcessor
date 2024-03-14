
from transactions_process_service.services.parsers.bank_parsers.forbright_bank_parser import ForbrightBankParser
from transactions_process_service.services.parsers.bank_parsers.united_bank_parser import UnitedBankParser


all_parsers = {
    "united_bank": UnitedBankParser,
    "forbright_bank": ForbrightBankParser,}