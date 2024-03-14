import logging
from transactions_process_service.services.parsers.system_parsers.system_parser import (
    PharmBillsParser,
)
from transactions_process_service.services.parsers.bank_parsers.forbright_bank_parser import (
    ForbrightBankParser,
)
from transactions_process_service.services.transaction_matcher import (
    TransactionMathcher,
)

from transactions_process_service.services.excel_creator import ExcelController


def test_reconcile_forbright_bank():
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
    workbook_name = "tests/output_tests_data/transactions_output.xlsx"
    bank_name = "Bank"
    system_name = "PharmBills System"
    transaction_matcher = TransactionMathcher()
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
<<<<<<< Updated upstream
    formatted_bank_log_message = "\n".join(
        str(transaction_dict) for transaction_dict in bank_transactions
    )
    formatted_system_log_message = "\n".join(
        str(transaction_dict) for transaction_dict in system_transactions
    )
    # logger.info(formatted_log_message)
    logger.debug(f"{len(bank_transactions)} bank_transactions_formated \n{formatted_bank_log_message}\n\n")
    logger.debug(f"{len(system_transactions)} all_system_transactions \n{formatted_system_log_message}\n\n")
    
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
||||||| Stash base

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
=======

    print(f"one_to_ont: {len(perfect_matches)}")
    unmatched_s = len(unmatched_system_amounts)
    unmatched_b = len(unmatched_bank_amounts)
>>>>>>> Stashed changes

<<<<<<< Updated upstream
    excel_controller.create_transaction_excel(
        data, workbook_name, bank_name, system_name
    )
    logger.info("Test finished")
||||||| Stash base
    excel_controller.create_transaction_excel(
        data, workbook_name, bank_name, system_name
    )

=======
    for key, value in matches.items():
        unmatched_b -= 1
        unmatched_s -= len(value)

    print(f"unmatched_system: {unmatched_s}")
    print(f"unmatched_bank: {unmatched_b}")

    print(f"calculated unmatched_system: {len(unmatched_system_amounts)}")
    print(f"calculated unmatched_bank: {len(unmatched_bank_amounts)}")

    # data = {
    #     "transactions": {
    #         "system": system_transactions,
    #         "bank": bank_transactions,
    #     },
    #     "matches": {
    #         "one_to_one": perfect_matches,
    #         "multi_to_one": matches,
    #         "unmatched_system": unmatched_system_amounts,
    #         "unmatched_bank": unmatched_bank_amounts,
    #     },
    # }
    #
    # excel_controller.create_transaction_excel(
    #     data, workbook_name, bank_name, system_name
    # )

>>>>>>> Stashed changes
    assert True
