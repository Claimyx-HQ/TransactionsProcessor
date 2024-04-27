from transactions_process_service.services.parsers.bank_parsers.connect_one_bank_parser import ConnectOneBankParser
from transactions_process_service.services.parsers.bank_parsers.flagstar_bank_parser import FlagstarBankParser
from transactions_process_service.services.parsers.bank_parsers.forbright_bank_parser import (
    ForbrightBankParser,
)
from transactions_process_service.services.parsers.bank_parsers.servis1st_bank_parser import Servis1stBankParser
from transactions_process_service.services.parsers.bank_parsers.united_bank_parser import (
    UnitedBankParser,
)


all_parsers = {
    "United Bank": UnitedBankParser(),
    "Forbright": ForbrightBankParser(),
    "Connect One": ConnectOneBankParser(),
    "Flagstar": FlagstarBankParser(),
    "Servis1st": Servis1stBankParser(),
}
