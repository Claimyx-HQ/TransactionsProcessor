from typing import Dict
from transactions_processor.services.parsers.bank_parsers.amalgamated_bank_parser import (
    AmalgamatedBankParser,
)
from transactions_processor.services.parsers.bank_parsers.bank_feeds_parser import (
    BankFeedsParser,
)
from transactions_processor.services.parsers.bank_parsers.bank_of_america_merrill_lynch_parser import (
    BankOfAmericaMerrillLynchParser,
)
from transactions_processor.services.parsers.bank_parsers.bank_of_texas_parser import BankOfTexasParser
from transactions_processor.services.parsers.bank_parsers.bankwell_bank_parser import (
    BankWellBankParser,
)
from transactions_processor.services.parsers.bank_parsers.bhi_bank_parser import (
    BHIBankParser,
)
from transactions_processor.services.parsers.bank_parsers.cadence_bank_parser import (
    CadenceBankParser,
)
from transactions_processor.services.parsers.bank_parsers.capital_one_bank_parser import (
    CapitalOneBankParser,
)
from transactions_processor.services.parsers.bank_parsers.cfg_bank_parser import (
    CfgBankParser,
)
from transactions_processor.services.parsers.bank_parsers.chase_bank_parser import (
    ChaseBankParser,
)
from transactions_processor.services.parsers.bank_parsers.cibc_bank_parser import (
    CIBCBankParser,
)
from transactions_processor.services.parsers.bank_parsers.citizens_bank_parser import (
    CitizensBankParser,
)
from transactions_processor.services.parsers.bank_parsers.connect_one_bank_parser import (
    ConnectOneBankParser,
)
from transactions_processor.services.parsers.bank_parsers.customers_bank_parser import (
    CustomersBankParser,
)
from transactions_processor.services.parsers.bank_parsers.daca_bank_parser import (
    DACABankParser,
)
from transactions_processor.services.parsers.bank_parsers.first_financial_bank_parser import (
    FirstFinancialBankParser,
)
from transactions_processor.services.parsers.bank_parsers.first_united_bank_parser import (
    FirstUnitedBankParser,
)
from transactions_processor.services.parsers.bank_parsers.flagstar_bank_parser import (
    FlagstarBankParser,
)
from transactions_processor.services.parsers.bank_parsers.forbright_bank_parser import (
    ForbrightBankParser,
)
from transactions_processor.services.parsers.bank_parsers.hancock_whitney_bank_parser import (
    HancockWhitneyBankParser,
)
from transactions_processor.services.parsers.bank_parsers.huntington_bank_parser import (
    HuntingtonBankParser,
)
from transactions_processor.services.parsers.bank_parsers.key_bank_parser import (
    KeyBankParser,
)
from transactions_processor.services.parsers.bank_parsers.legend_bank_parser import (
    LegendBankParser,
)
from transactions_processor.services.parsers.bank_parsers.metropolitan_bank_parser import (
    MetropolitanBankParser,
)
from transactions_processor.services.parsers.bank_parsers.midfirst_bank_parser import (
    MidFirstBankParser,
)
from transactions_processor.services.parsers.bank_parsers.midwest_bank_parser import (
    MidwestBankParser,
)
from transactions_processor.services.parsers.bank_parsers.old_national_bank_parser import (
    OldNationalBankParser,
)
from transactions_processor.services.parsers.bank_parsers.pnc_bank_parser import (
    PNCBankParser,
)
from transactions_processor.services.parsers.bank_parsers.popular_bank_parser import (
    PopularBankParser,
)
from transactions_processor.services.parsers.bank_parsers.regions_bank_parser import (
    RegionsBankParser,
)
from transactions_processor.services.parsers.bank_parsers.servis1st_bank_parser import (
    Servis1stBankParser,
)
from transactions_processor.services.parsers.bank_parsers.simmons_bank_parser import (
    SimmonsBankParser,
)
from transactions_processor.services.parsers.bank_parsers.state_bank_parser import (
    StateBankParser,
)
from transactions_processor.services.parsers.bank_parsers.sunflower_bank_parser import (
    SunflowerBankParser,
)
from transactions_processor.services.parsers.bank_parsers.the_berkshire_bank_parser import (
    TheBerkshireBankParser,
)
from transactions_processor.services.parsers.bank_parsers.tomball_baylor_bank_parser import (
    TomballBaylorBankParser,
)
from transactions_processor.services.parsers.bank_parsers.truist_bank_parser import (
    TruistBankParser,
)
from transactions_processor.services.parsers.bank_parsers.united_bank_parser import (
    UnitedBankParser,
)
from transactions_processor.services.parsers.bank_parsers.valley_bank_parser import (
    ValleyBankParser,
)
from transactions_processor.services.parsers.bank_parsers.vera_bank_parser import (
    VeraBankParser,
)
from transactions_processor.services.parsers.bank_parsers.vista_bank_parser import (
    VistaBankParser,
)
from transactions_processor.services.parsers.bank_parsers.webster_bank_parser import (
    WebsterBankParser,
)
from transactions_processor.services.parsers.bank_parsers.wells_fargo_bank_parser import (
    WellsFargoBankParser,
)
from transactions_processor.services.parsers.bank_parsers.workday_bank_feeds_parser import WorkdayBankFeedsParser
from transactions_processor.services.parsers.transactions_parser import (
    TransactionsParser,
)

bank_parsers: Dict[str, type[TransactionsParser]] = {
    "amalgamated": AmalgamatedBankParser,
    "bank_feed": BankFeedsParser,
    "bank_of_america": BankOfAmericaMerrillLynchParser,
    "bank_of_texas": BankOfTexasParser,
    "workday_bank_feeds": WorkdayBankFeedsParser,
    "bhi": BHIBankParser,
    "bankwell": BankWellBankParser,
    "bok_financial": BankOfTexasParser,
    "cadence": CadenceBankParser,
    "capital_one": CapitalOneBankParser,
    "cfg": CfgBankParser,
    "chase": ChaseBankParser,
    "cibc": CIBCBankParser,
    "citizens": CitizensBankParser,
    "connect_one": ConnectOneBankParser,
    "customers": CustomersBankParser,
    "daca": DACABankParser,
    "first_financial": FirstFinancialBankParser,
    "first_united": FirstUnitedBankParser,
    "flagstar": FlagstarBankParser,
    "forbright": ForbrightBankParser,
    "hancock": HancockWhitneyBankParser,
    "huntington": HuntingtonBankParser,
    "key": KeyBankParser,
    "legend": LegendBankParser,
    "metropolitan": MetropolitanBankParser,
    "midfirst": MidFirstBankParser,
    "midwest": MidwestBankParser,
    "old_national": OldNationalBankParser,
    "pnc": PNCBankParser,
    "popular": PopularBankParser,
    "regions": RegionsBankParser,
    "servis1st": Servis1stBankParser,
    "simmons": SimmonsBankParser,
    "state": StateBankParser,
    "sunflower": SunflowerBankParser,
    "the_berkshire": TheBerkshireBankParser,
    "tomball_baylor": TomballBaylorBankParser,
    "truist": TruistBankParser,
    "united": UnitedBankParser,
    "valley": ValleyBankParser,
    "vera": VeraBankParser,
    "vista": VistaBankParser,
    "webster": WebsterBankParser,
    "wells_fargo": WellsFargoBankParser,
}
