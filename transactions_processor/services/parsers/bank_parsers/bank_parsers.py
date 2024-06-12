
from transactions_processor.services.parsers.bank_parsers.bhi_bank_parser import BHIBankParser
from transactions_processor.services.parsers.bank_parsers.cibc_bank_parser import CIBCBankParser
from transactions_processor.services.parsers.bank_parsers.connect_one_bank_parser import ConnectOneBankParser
from transactions_processor.services.parsers.bank_parsers.daca_bank_parser import DACABankParser
from transactions_processor.services.parsers.bank_parsers.flagstar_bank_parser import FlagstarBankParser
from transactions_processor.services.parsers.bank_parsers.forbright_bank_parser import ForbrightBankParser
from transactions_processor.services.parsers.bank_parsers.huntington_bank_parser import HuntingtonBankParser
from transactions_processor.services.parsers.bank_parsers.midwest_bank_parser import MidwestBankParser
from transactions_processor.services.parsers.bank_parsers.pnc_bank_parser import PNCBankParser
from transactions_processor.services.parsers.bank_parsers.popular_bank_parser import PopularBankParser
from transactions_processor.services.parsers.bank_parsers.servis1st_bank_parser import Servis1stBankParser
from transactions_processor.services.parsers.bank_parsers.united_bank_parser import UnitedBankParser
from transactions_processor.services.parsers.bank_parsers.webster_bank_parser import WebsterBankParser
from transactions_processor.services.parsers.bank_parsers.wells_fargo_bank_parser import WellsFargoBankParser

bank_parsers = {
    'cibc': CIBCBankParser,
    'connect_one': ConnectOneBankParser,
    'daca': DACABankParser,
    'flagstar': FlagstarBankParser,
    'forbright': ForbrightBankParser,
    'huntington': HuntingtonBankParser,
    'pnc': PNCBankParser,
    'popular': PopularBankParser,
    'servis1st': Servis1stBankParser,
    'united': UnitedBankParser,
    'webster': WebsterBankParser,
    'wells_fargo': WellsFargoBankParser,
    'bhi': BHIBankParser,
    'midwest': MidwestBankParser
}
