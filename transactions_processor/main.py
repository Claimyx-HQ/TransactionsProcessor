import json
from typing import List
import uuid
import boto3
import concurrent.futures
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.excel.excel_controller import ExcelController
import logging
import io
from transactions_processor.services.parsers.bank_parsers.bank_parsers import bank_parsers
from transactions_processor.services.parsers.system_parsers.system_parsers import system_parsers

from transactions_processor.services.transaction_matcher import TransactionMatcher
from transactions_processor.utils.aws_utils import upload_file_to_s3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bank_name = "Bank"
    system_name = "PharmBills System"
    body = json.loads(event['body'])
    system_transactions_data = body['system_file']
    bank_transactions_data = body['bank_files']
    bucket_name = 'bankrectool-files'

    transaction_matcher = TransactionMatcher()
    excel_controller = ExcelController()
    
    # Create a thread pool executor
    generated_excel: io.BytesIO | None
    with concurrent.futures.ThreadPoolExecutor() as executor:
        system_file = retrieve_file(bucket_name, system_transactions_data['key'])
        # system_file_task = executor.submit(retrieve_file, bucket_name, system_transactions_data['key'])
        bank_files_tasks = [executor.submit(retrieve_file, bucket_name, bank_file['key']) for bank_file in bank_transactions_data]
        concurrent.futures.wait(bank_files_tasks)

        system_parser = system_parsers[system_transactions_data['type']]()
        system_transactions = system_parser.parse_transactions(system_file)
        initialized_bank_parsers = {}
        all_bank_transactions = []
        for i in range(len(bank_files_tasks)):
            print('Parsing bank')
            bank_type = bank_transactions_data[i]['type']
            if bank_type not in initialized_bank_parsers:
                initialized_bank_parsers[bank_type] = bank_parsers[bank_type]()
            bank_parser = initialized_bank_parsers[bank_type]
            bank_file = bank_files_tasks[i].result()
            bank_transactions = bank_parser.parse_transactions(bank_file)
            all_bank_transactions.extend(bank_transactions)
            print('Bank type:', bank_type)
            print(bank_transactions)

        data = find_matches(
            all_bank_transactions, system_transactions, transaction_matcher
        )

        generated_excel = excel_controller.create_transaction_excel(
            data, None, bank_name, system_name
        )
    
    # Construct the response
    if generated_excel is None:
        response = {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*',
                'Access-Control-Allow-Headers': '*',
            },
            'body': json.dumps({'message': 'Error processing files'})
        }
        return response


    presigned_url = upload_file_to_s3(
        s3, 
        generated_excel, 
        bucket_name, 
        f'{uuid.uuid4()}.xlsx'
    )

    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Headers': '*',
            # 'Content-Disposition': 'attachment; filename="transactions_result.xlsx"',
            # 'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        },
        'body': json.dumps({'presigned_url': presigned_url})
        # 'body': generated_excel.getvalue(),
        # 'isBase64Encoded': True
    }
    
    return response


def retrieve_file(bucket_name, key):
    # Download the file from S3
    file_obj = s3.get_object(Bucket=bucket_name, Key=key)
    file_content = file_obj['Body'].read()
    file = io.BytesIO(file_content)
    print(f'Read file, length: {len(file_content)}')
    return file
    

def download_and_process_file(bucket_name, key):
    # Download the file from S3
    file_obj = s3.get_object(Bucket=bucket_name, Key=key)
    file_content = file_obj['Body'].read()
    print(file_content)
    
    # Process the file content (replace with your own logic)
    processed_content = process_file(file_content)
    
    # Save the processed file back to S3 (optional)
    processed_key = f"processed/{key}"
    s3.put_object(Bucket=bucket_name, Key=processed_key, Body=processed_content)

def process_file(file_content):
    # Your file processing logic goes here
    # This is just a placeholder example
    processed_content = file_content.upper()
    return processed_content



def find_matches(
    all_bank_transactions: List[Transaction],
    system_transactions: List[Transaction],
    transaction_matcher: TransactionMatcher,
):
    logger = logging.getLogger(__name__)
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
    (
        matches,
        unmatched_bank_amounts,
        unmatched_system_amounts,
    ) = transaction_matcher.find_reconciling_matches(
        unmatched_bank_amounts, unmatched_system_amounts
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
