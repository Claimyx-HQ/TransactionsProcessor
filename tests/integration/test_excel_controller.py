import logging
from transactions_process_service.services.parsers.bank_parsers.connect_one_bank_parser import ConnectOneBankParser
from transactions_process_service.services.parsers.bank_parsers.flagstar_bank_parser import FlagstarBankParser
from transactions_process_service.services.parsers.system_parsers.system_parser import (
    PharmBillsParser,
)
from transactions_process_service.services.parsers.bank_parsers.united_bank_parser import (
    UnitedBankParser,
)
from transactions_process_service.services.parsers.bank_parsers.forbright_bank_parser import (
    ForbrightBankParser,
)
from transactions_process_service.services.transaction_matcher import (
    TransactionMatcher
)

from transactions_process_service.services.excel_creation.excel_controller import ExcelController


def test_excel_controller_with_united_bank():
    logging.basicConfig(
        filename="tests.log",
        filemode="w",
        format="%(asctime)s %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
    )
    logger = logging.getLogger(__name__)
    logger.info("App started")
    bank_file_path = "tests/data/united_bank.pdf"
    system_file_path = "tests/data/bankst.xls"
    workbook_name = "tests/output_tests_data/united_transactions_output.xlsx"
    bank_name = "Bank"
    system_name = "PharmBills System"
    transaction_matcher = TransactionMatcher()
    bank_parser = UnitedBankParser()
    system_parser = PharmBillsParser()
    excel_controller = ExcelController()

    bank_transactions = bank_parser.parse_transactions(bank_file_path)
    system_transactions = system_parser.parse_transactions(system_file_path)

    (
        perfect_matches,
        unmatched_bank_amounts,
        unmatched_system_amounts,
    ) = transaction_matcher.find_matched_unmatched(
        [t.amount for t in bank_transactions], [t.amount for t in system_transactions]
    )

    (
        matches,
        unmatched_bank_amounts,
        unmatched_system_amounts,
    ) = transaction_matcher.find_reconciling_matches(
        unmatched_bank_amounts, unmatched_system_amounts
    )
    formatted_bank_log_message = "\n".join(
        str(transaction_dict) for transaction_dict in bank_transactions
    )
    formatted_system_log_message = "\n".join(
        str(transaction_dict) for transaction_dict in system_transactions
    )
    # logger.info(formatted_log_message)
    logger.debug(
        f"{len(bank_transactions)} bank_transactions_formated \n{formatted_bank_log_message}\n\n"
    )
    logger.debug(
        f"{len(system_transactions)} all_system_transactions \n{formatted_system_log_message}\n\n"
    )

    data = {
        "transactions": {
            "system": system_transactions,
            "bank": bank_transactions,
        },
        "matches": {
            "one_to_one": perfect_matches,
            "multi_to_one": matches,
            "unmatched_system": unmatched_system_amounts,
            "unmatched_bank": unmatched_bank_amounts,
        },
    }
    logger.debug(
        f"Data for excel :one_to_one: {len(perfect_matches)},multi_to_one: {len(matches)},unmatched_system: {len(unmatched_system_amounts)}, unmatched_bank: {len(unmatched_bank_amounts)}"
    )
    excel_controller.create_transaction_excel(
        data, workbook_name, bank_name, system_name
    )

    logger.info("Test finished")

    assert True



def test_excel_controller_with_forbright_bank():
    logging.basicConfig(
        filename="tests.log",
        filemode="w",
        format="%(asctime)s %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
    )
    logger = logging.getLogger(__name__)
    logger.info("App started")
    bank_file_path = "tests/data/forbright_bank.pdf"
    system_file_path = "tests/data/bankst.xls"
    workbook_name = "tests/output_tests_data/forbright_transactions_output.xlsx"
    bank_name = "Bank"
    system_name = "PharmBills System"
    transaction_matcher = TransactionMatcher()
    bank_parser = ForbrightBankParser()
    system_parser = PharmBillsParser()
    excel_controller = ExcelController()

    bank_transactions = bank_parser.parse_transactions(bank_file_path)
    system_transactions = system_parser.parse_transactions(system_file_path)

    (
        perfect_matches,
        unmatched_bank_amounts,
        unmatched_system_amounts,
    ) = transaction_matcher.find_matched_unmatched(
        [t.amount for t in bank_transactions], [t.amount for t in system_transactions]
    )

    (
        matches,
        unmatched_bank_amounts,
        unmatched_system_amounts,
    ) = transaction_matcher.find_reconciling_matches(
        unmatched_bank_amounts, unmatched_system_amounts
    )
    formatted_bank_log_message = "\n".join(
        str(transaction_dict) for transaction_dict in bank_transactions
    )
    formatted_system_log_message = "\n".join(
        str(transaction_dict) for transaction_dict in system_transactions
    )
    # logger.info(formatted_log_message)
    logger.debug(
        f"{len(bank_transactions)} bank_transactions_formated \n{formatted_bank_log_message}\n\n"
    )
    logger.debug(
        f"{len(system_transactions)} all_system_transactions \n{formatted_system_log_message}\n\n"
    )

    data = {
        "transactions": {
            "system": system_transactions,
            "bank": bank_transactions,
        },
        "matches": {
            "one_to_one": perfect_matches,
            "multi_to_one": matches,
            "unmatched_system": unmatched_system_amounts,
            "unmatched_bank": unmatched_bank_amounts,
        },
    }
    logger.debug(
        f"Data for excel :one_to_one: {len(perfect_matches)},multi_to_one: {len(matches)},unmatched_system: {len(unmatched_system_amounts)}, unmatched_bank: {len(unmatched_bank_amounts)}"
    )
    excel_controller.create_transaction_excel(
        data, workbook_name, bank_name, system_name
    )

    logger.info("Test finished")

    assert True

def test_excel_controller_with_flagstar_bank():
    logging.basicConfig(
        filename="tests.log",
        filemode="w",
        format="%(asctime)s %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
    )
    logger = logging.getLogger(__name__)
    logger.info("App started")
    bank_file_path = "tests/data/flagstar/flagstar_bank.pdf"
    system_file_path = "tests/data/flagstar/_actgsmry_lotusvilla_test.xls"
    workbook_name = "tests/output_tests_data/flagstar_transactions_output.xlsx"
    bank_name = "Bank"
    system_name = "PharmBills System"
    transaction_matcher = TransactionMatcher()
    bank_parser = FlagstarBankParser()
    system_parser = PharmBillsParser()
    excel_controller = ExcelController()

    bank_transactions = bank_parser.parse_transactions(bank_file_path)
    system_transactions = system_parser.parse_transactions(system_file_path)

    (
        perfect_matches,
        unmatched_bank_amounts,
        unmatched_system_amounts,
    ) = transaction_matcher.find_matched_unmatched(
        [t.amount for t in bank_transactions], [t.amount for t in system_transactions]
    )

    (
        matches,
        unmatched_bank_amounts,
        unmatched_system_amounts,
    ) = transaction_matcher.find_reconciling_matches(
        unmatched_bank_amounts, unmatched_system_amounts
    )
    formatted_bank_log_message = "\n".join(
        str(transaction_dict) for transaction_dict in bank_transactions
    )
    formatted_system_log_message = "\n".join(
        str(transaction_dict) for transaction_dict in system_transactions
    )
    # logger.info(formatted_log_message)
    logger.debug(
        f"{len(bank_transactions)} bank_transactions_formated \n{formatted_bank_log_message}\n\n"
    )
    logger.debug(
        f"{len(system_transactions)} all_system_transactions \n{formatted_system_log_message}\n\n"
    )

    data = {
        "transactions": {
            "system": system_transactions,
            "bank": bank_transactions,
        },
        "matches": {
            "one_to_one": perfect_matches,
            "multi_to_one": matches,
            "unmatched_system": unmatched_system_amounts,
            "unmatched_bank": unmatched_bank_amounts,
        },
    }
    logger.debug(
        f"Data for excel :one_to_one: {len(perfect_matches)},multi_to_one: {len(matches)},unmatched_system: {len(unmatched_system_amounts)}, unmatched_bank: {len(unmatched_bank_amounts)}"
    )
    excel_controller.create_transaction_excel(
        data, workbook_name, bank_name, system_name
    )

    logger.info("Test finished")

    assert True

def test_excel_controller_with_connect_one_bank():
    logging.basicConfig(
        filename="tests.log",
        filemode="w",
        format="%(asctime)s %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
    )
    logger = logging.getLogger(__name__)
    logger.info("App started")
    bank_file_path = "tests/data/connect_one/connect_one_bank.pdf"
    system_file_path = "tests/data/connect_one/ncs_excell_statement_blue.xls"
    workbook_name = "tests/output_tests_data/connect_one_transactions_output.xlsx"
    bank_name = "Bank"
    system_name = "PharmBills System"
    transaction_matcher = TransactionMatcher()
    bank_parser = ConnectOneBankParser()
    system_parser = PharmBillsParser()
    excel_controller = ExcelController()

    bank_transactions = bank_parser.parse_transactions(bank_file_path)
    system_transactions = system_parser.parse_transactions(system_file_path)

    (
        perfect_matches,
        unmatched_bank_amounts,
        unmatched_system_amounts,
    ) = transaction_matcher.find_matched_unmatched(
        [t.amount for t in bank_transactions], [t.amount for t in system_transactions]
    )

    (
        matches,
        unmatched_bank_amounts,
        unmatched_system_amounts,
    ) = transaction_matcher.find_reconciling_matches(
        unmatched_bank_amounts, unmatched_system_amounts
    )
    formatted_bank_log_message = "\n".join(
        str(transaction_dict) for transaction_dict in bank_transactions
    )
    formatted_system_log_message = "\n".join(
        str(transaction_dict) for transaction_dict in system_transactions
    )
    # logger.info(formatted_log_message)
    logger.debug(
        f"{len(bank_transactions)} bank_transactions_formated \n{formatted_bank_log_message}\n\n"
    )
    logger.debug(
        f"{len(system_transactions)} all_system_transactions \n{formatted_system_log_message}\n\n"
    )

    data = {
        "transactions": {
            "system": system_transactions,
            "bank": bank_transactions,
        },
        "matches": {
            "one_to_one": perfect_matches,
            "multi_to_one": matches,
            "unmatched_system": unmatched_system_amounts,
            "unmatched_bank": unmatched_bank_amounts,
        },
    }
    logger.debug(
        f"Data for excel :one_to_one: {len(perfect_matches)},multi_to_one: {len(matches)},unmatched_system: {len(unmatched_system_amounts)}, unmatched_bank: {len(unmatched_bank_amounts)}"
    )
    excel_controller.create_transaction_excel(
        data, workbook_name, bank_name, system_name
    )

    logger.info("Test finished")

    assert True