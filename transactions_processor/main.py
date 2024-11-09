import asyncio
import json
import requests
from typing import List
import uuid
import concurrent.futures
from transactions_processor.schemas.analysis_request import (
    AnalysisRequest,
    AnalysisRequestCreate,
)
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.analysis_requests_service import (
    AnalysisRequestsService,
)
from transactions_processor.services.excel.excel_controller import ExcelController
from transactions_processor.services.parsers.bank_parsers.bank_parsers import (
    bank_parsers,
)
from transactions_processor.services.parsers.system_parsers.system_parsers import (
    system_parsers,
)

from transactions_processor.services.parsers.transactions_parser import (
    TransactionsParser,
)
from transactions_processor.services.reconciliation.transactions_matcher import (
    TransactionsMatcher,
)
from transactions_processor.utils.aws_utils import (
    generate_error_code,
    notify_client,
    retrieve_file,
    upload_file_to_s3,
)
import multiprocessing
from loguru import logger


bank_name = "Bank"
system_name = "PharmBills System"
bucket_name = "bankrectool-files"


def lambda_handler(event, context):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(async_handler(event, context))


async def async_handler(event, context):
    client_id: str | None = None
    analysis_request: AnalysisRequest | None = None
    analysis_requests_service = AnalysisRequestsService()
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        },
        "body": None,
    }

    try:
        logger.info(f"Received event: {event}")

        system_transactions_data, bank_transactions_data, client_id = (
            parse_lambda_event(event)
        )

        if not client_id:
            raise Exception("Client ID is required")

        transaction_matcher = TransactionsMatcher()
        excel_controller = ExcelController()

        analysis_request = await analysis_requests_service.create_request(
            AnalysisRequestCreate(
                user_id=client_id,
                request_type="reconciliation",
                status="processing",
                parameters={
                    "system_file": system_transactions_data,
                    "bank_files": bank_transactions_data,
                },
            )
        )

        logger.debug("Retrieving files from s3")

        update_progress(client_id, "Processing", 0, str(analysis_request.id))

        system_data, banks_data = retrieve_files(
            bucket_name, system_transactions_data, bank_transactions_data
        )

        logger.debug(
            f'Parsing transactions, system: {system_data["name"]}, bank: {len(banks_data)}'
        )

        system_transactions, bank_transactions = parse_transactions(
            system_data, banks_data
        )

        logger.debug(
            f"Transactions parsed, system: {len(system_transactions)}, bank: {len(bank_transactions)}"
        )

        data = find_matches(
            client_id,
            str(analysis_request.id),
            bank_transactions,
            system_transactions,
            transaction_matcher,
        )

        generated_excel = excel_controller.create_transaction_excel(
            data, None, bank_name, system_name
        )

        # Construct the response
        if generated_excel is None:
            raise Exception("Failed to generate excel file")

        result_file_key = f"{uuid.uuid4()}.xlsx"
        presigned_url = upload_file_to_s3(generated_excel, bucket_name, result_file_key)

        await analysis_requests_service.complete_request(
            str(analysis_request.id),
            {
                "matches": {
                    "one_to_one": len(data["matches"]["one_to_one"]),
                    "multi_to_one": len(data["matches"]["multi_to_one"]),
                    "unmatched_system": len(data["matches"]["unmatched_system"]),
                    "unmatched_bank": len(data["matches"]["unmatched_bank"]),
                },
                "result_file_key": result_file_key,
            },
        )

        response["body"] = json.dumps({"presigned_url": presigned_url})

        notify_client(
            client_id,
            {
                "message": "Processing complete",
                "url": presigned_url,
                "request_id": str(analysis_request.id),
            },
        )

        logger.info(
            f"Successfully processed transactions, system_data: {system_transactions_data}, bank_data: {bank_transactions_data}"
        )

    except Exception as e:
        error_code = generate_error_code(e)
        logger.error(
            f"Failed to process transactions: {e}, error code: {error_code}, event: {event}"
        )
        if analysis_request:
            await analysis_requests_service.fail_request(
                str(analysis_request.id), {"error": str(e), "error_code": error_code}
            )

        notify_client(
            client_id,
            {
                "message": "error",
                "request_id": str(analysis_request.id if analysis_request else ""),
                "error": "Processing failed",
                "error_code": error_code,
            },
        )

    finally:
        return response


def parse_lambda_event(event):
    body = json.loads(event["Records"][0]["body"])
    system_transactions_data = body["system_file"]
    bank_transactions_data = body["bank_files"]
    client_id = body["client_id"]
    return system_transactions_data, bank_transactions_data, client_id


def retrieve_files(bucket_name, system_transactions_data, bank_transactions_data):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        raw_system_file = retrieve_file(bucket_name, system_transactions_data["key"])

        system_file = {
            "key": system_transactions_data["key"],
            "file": raw_system_file,
            "type": system_transactions_data["type"],
            "name": system_transactions_data["name"],
        }
        # system_file_task = executor.submit(retrieve_file, bucket_name, system_transactions_data['key'])
        bank_files_tasks = [
            executor.submit(retrieve_file, bucket_name, bank_file["key"])
            for bank_file in bank_transactions_data
        ]
        concurrent.futures.wait(bank_files_tasks)
        bank_files = []
        for i in range(len(bank_files_tasks)):
            bank_files.append(
                {
                    "key": bank_transactions_data[i]["key"],
                    "file": bank_files_tasks[i].result(),
                    "type": bank_transactions_data[i]["type"],
                    "name": bank_transactions_data[i]["name"],
                }
            )
        # bank_files = [
        #     {"key": bank_file["key"], "file": task.result()}
        #     for bank_file, task in zip(bank_transactions_data, bank_files_tasks)
        # ]
        # bank_files = [task.result() for task in bank_files_tasks]
    return system_file, bank_files


def parse_transactions(system_data, banks_data):
    # TODO: This also needs to run in parallel
    system_parser: TransactionsParser = system_parsers[system_data["type"]]()
    system_transactions = system_parser.parse_transactions(
        system_data["file"],
        system_data["name"],
        system_data["key"],
    )
    bank_transactions = []
    for i in range(len(banks_data)):
        bank_type = banks_data[i]["type"]
        bank_file_key = banks_data[i]["key"]
        bank_file_name = banks_data[i]["name"]
        bank_file = banks_data[i]["file"]
        bank_parser: TransactionsParser = bank_parsers[bank_type]()
        parsed_bank_transactions = bank_parser.parse_transactions(
            bank_file, bank_file_name, bank_file_key
        )
        bank_transactions.extend(parsed_bank_transactions)
    return system_transactions, bank_transactions


def process_file(file_content):
    # Your file processing logic goes here
    # This is just a placeholder example
    processed_content = file_content.upper()
    return processed_content


def find_matches(
    client_id: str,
    request_id: str,
    all_bank_transactions: List[Transaction],
    system_transactions: List[Transaction],
    transaction_matcher: TransactionsMatcher,
):
    system_amounts = [transaction.amount for transaction in system_transactions]
    update_progress(client_id, "Matching", 0, request_id)
    logger.debug(
        f"Finding matches, system: {len(system_transactions)}, bank: {len(all_bank_transactions)}"
    )
    matched_transactions = transaction_matcher.find_one_to_one_matches(
        all_bank_transactions, system_transactions
    )

    # TODO: this is a hack until excel parser will handle transactions instead of amounts
    perfect_matches = [
        transaction[0].amount for transaction in matched_transactions.matched
    ]
    unmatched_bank_amounts = [
        transaction.amount for transaction in matched_transactions.unmatched_bank
    ]
    unmatched_system_amounts = [
        transaction.amount for transaction in matched_transactions.unmatched_system
    ]
    zero_and_negative_system_amounts = [
        amount for amount in unmatched_system_amounts if amount <= 0
    ]
    unmatched_system_amounts = [
        amount for amount in unmatched_system_amounts if amount > 0
    ]

    logger.debug(f"Matching complete, perfect matches: {len(perfect_matches)}")

    update_progress(client_id, "Matching", 100, request_id)
    update_progress(client_id, "Reconciling", 0, request_id)

    # (
    #     matches,
    #     unmatched_bank_amounts,
    #     unmatched_system_amounts,
    # ) = transaction_matcher.find_reconciling_matches(
    #     unmatched_bank_amounts,
    #     unmatched_system_amounts,
    #     lambda progress: update_progress(
    #         client_id, "Reconciling", progress, request_id
    #     ),
    # )
    #
    logger.debug(f"perfect matches: {perfect_matches}")
    logger.debug(
        f"finding matches for banks: {unmatched_bank_amounts},\n system: {unmatched_system_amounts}"
    )
    multi_matches = transaction_matcher.find_one_to_many_matches(
        matched_transactions.unmatched_bank,
        matched_transactions.unmatched_system,
    )

    matches = {}
    for transaction in multi_matches.matched:
        matches[transaction[0][0].amount] = [t.amount for t in transaction[1]]
    unmatched_system_amounts = [
        transaction.amount for transaction in multi_matches.unmatched_system
    ]
    unmatched_bank_amounts = [
        transaction.amount for transaction in multi_matches.unmatched_bank
    ]

    # TODO: this is a hack until excel parser will handle transactions instead of amounts
    unmatched_system_amounts.extend(zero_and_negative_system_amounts)

    logger.info(
        f"""
        "transactions": "system": {len(system_transactions)}, "bank": {len(all_bank_transactions)},
        "matches": 
            "one_to_one": {len(perfect_matches)},
            "multi_to_one": {len(matches)},
            "unmatched_system": {len(unmatched_system_amounts)},
            "unmatched_bank": {len(unmatched_bank_amounts)},
        ,
    """
    )
    return {
        "transactions": {"system": system_transactions, "bank": all_bank_transactions},
        "matches": {
            "one_to_one": perfect_matches,
            "multi_to_one": matches,
            "unmatched_system": unmatched_system_amounts,
            "unmatched_bank": unmatched_bank_amounts,
        },
    }


def update_progress_thread(
    self, total_transactions: int, progress_queue: multiprocessing.Queue
):
    while not self.stop_progress_thread.is_set():
        try:
            # This will block until an item is available
            progress_increment = progress_queue.get(timeout=1)
            with self.progress_lock:
                self.progress += progress_increment
                progress_percentage = (self.progress / total_transactions) * 100
            self.update_client_progress(progress_percentage)
        except Exception as e:
            # If no progress update in 1 second, just continue
            continue


def update_progress(client_id, type, progress, request_id):
    notify_client(
        client_id,
        {
            "message": "progress",
            "request_id": request_id,
            "type": type,
            "progress": progress,
        },
        timeout=1,
    )
