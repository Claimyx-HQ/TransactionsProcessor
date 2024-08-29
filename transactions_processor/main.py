import json
import requests
from typing import List
import uuid
import concurrent.futures
from transactions_processor.exceptions.file_exceptions import UnreadableFileException
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.default_transactions_matcher import (
    DefaultTransactionsMatcher,
)
from transactions_processor.services.excel.excel_controller import ExcelController
import logging
import io
from transactions_processor.services.parallel_transactions_matcher import (
    ParallelTransactionsMatcher,
)
from transactions_processor.services.parsers.bank_parsers.bank_parsers import (
    bank_parsers,
)
from transactions_processor.services.parsers.system_parsers.system_parsers import (
    system_parsers,
)

from transactions_processor.services.parsers.transactions_parser import (
    TransactionsParser,
)
from transactions_processor.services.transactions_matcher import TransactionsMatcher
from transactions_processor.utils.aws_utils import (
    generate_error_code,
    notify_client,
    retrieve_file,
    upload_file_to_s3,
)
import multiprocessing


def lambda_handler(event, context):
    client_id: str | None = None

    try:
        bank_name = "Bank"
        system_name = "PharmBills System"
        body = json.loads(event["Records"][0]["body"])
        system_transactions_data = body["system_file"]
        bank_transactions_data = body["bank_files"]
        client_id = body["client_id"]
        bucket_name = "bankrectool-files"

        if not client_id:
            raise Exception("Client ID is required")

        transaction_matcher = ParallelTransactionsMatcher()
        excel_controller = ExcelController()

        # Create a thread pool executor
        bank_files = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            update_progress(client_id, "Processing", 0)
            system_file = retrieve_file(bucket_name, system_transactions_data["key"])
            # system_file_task = executor.submit(retrieve_file, bucket_name, system_transactions_data['key'])
            bank_files_tasks = [
                executor.submit(retrieve_file, bucket_name, bank_file["key"])
                for bank_file in bank_transactions_data
            ]
            concurrent.futures.wait(bank_files_tasks)
            for i in range(len(bank_files_tasks)):
                bank_files.append(
                    {
                        "key": bank_transactions_data[i]["key"],
                        "file": bank_files_tasks[i].result(),
                        "type": bank_transactions_data[i]["type"],
                        "extension": bank_transactions_data[i]["extension"],
                    }
                )
            # bank_files = [
            #     {"key": bank_file["key"], "file": task.result()}
            #     for bank_file, task in zip(bank_transactions_data, bank_files_tasks)
            # ]
            # bank_files = [task.result() for task in bank_files_tasks]

        # TODO: This also needs to run in parallel
        system_parser: TransactionsParser = system_parsers[
            system_transactions_data["type"]
        ]()
        system_transactions = system_parser.parse_transactions(
            system_file,
            system_transactions_data["extension"],
            system_transactions_data["key"],
        )
        initialized_bank_parsers = {}
        all_bank_transactions = []
        for i in range(len(bank_files)):
            bank_type = bank_files[i]["type"]
            bank_file_key = bank_files[i]["key"]
            bank_file_extension = bank_files[i]["extension"]
            bank_file = bank_files[i]["file"]
            if bank_type not in initialized_bank_parsers:
                initialized_bank_parsers[bank_type] = bank_parsers[bank_type]()
            bank_parser: TransactionsParser = initialized_bank_parsers[bank_type]
            bank_transactions = bank_parser.parse_transactions(
                bank_file, bank_file_extension, bank_file_key
            )
            all_bank_transactions.extend(bank_transactions)

        data = find_matches(
            client_id,
            all_bank_transactions,
            system_transactions,
            transaction_matcher,
        )

        generated_excel = excel_controller.create_transaction_excel(
            data, None, bank_name, system_name
        )

        # Construct the response
        if generated_excel is None:
            print(f"Failed to generate excel file for client {client_id}, body: {body}")
            response = {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "*",
                    "Access-Control-Allow-Headers": "*",
                },
            }
            return response

        presigned_url = upload_file_to_s3(
            generated_excel, bucket_name, f"{uuid.uuid4()}.xlsx"
        )

        response = {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*",
            },
            "body": json.dumps({"presigned_url": presigned_url}),
        }

        notify_client(
            client_id, {"message": "Processing complete", "url": presigned_url}
        )

        print(f"Successfully processed transactions, body: {body}")

        return response
    except Exception as e:
        error_code = generate_error_code(e)
        print(
            f"Failed to process transactions: {e}, error code: {error_code}, event: {event}"
        )
        if client_id:
            notify_client(
                client_id,
                {
                    "message": "error",
                    "error": "Processing failed",
                    "error_code": error_code,
                },
            )

        response = {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*",
            },
        }
        return response


def process_file(file_content):
    # Your file processing logic goes here
    # This is just a placeholder example
    processed_content = file_content.upper()
    return processed_content


def find_matches(
    client_id: str,
    all_bank_transactions: List[Transaction],
    system_transactions: List[Transaction],
    transaction_matcher: TransactionsMatcher,
):
    logger = logging.getLogger(__name__)
    update_progress(client_id, "Matching", 0)
    (
        perfect_matches,
        unmatched_bank_amounts,
        unmatched_system_amounts,
    ) = transaction_matcher.find_matched_unmatched(
        [t.amount for t in all_bank_transactions],
        [t.amount for t in system_transactions],
    )
    zero_and_negative_system_amounts = [
        amount for amount in unmatched_system_amounts if amount <= 0
    ]
    unmatched_system_amounts = [
        amount for amount in unmatched_system_amounts if amount > 0
    ]

    update_progress(client_id, "matching", 100)

    (
        matches,
        unmatched_bank_amounts,
        unmatched_system_amounts,
    ) = transaction_matcher.find_reconciling_matches(
        unmatched_bank_amounts,
        unmatched_system_amounts,
        lambda progress: update_progress(client_id, "Reconciling", progress),
    )
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


def update_progress(client_id, type, progress):
    notify_client(
        client_id,
        {
            "message": "progress",
            "type": type,
            "progress": progress,
        },
        timeout=1,
    )
