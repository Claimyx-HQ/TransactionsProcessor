from transactions_processor.services.parsers.system_parsers.ncs_parser import NCSParser
from transactions_processor.services.parsers.system_parsers.pcc.pcc_parser import (
    PCCParser,
)

system_parsers = {"ncs": NCSParser, "pcc": PCCParser}
