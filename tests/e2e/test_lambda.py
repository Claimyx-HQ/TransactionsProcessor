from transactions_processor.main import lambda_handler
import json


def test_lambda_hander():
    system_transactions_data = {
        "key": "bankst.xls",
        "type": "ncs",
        "name": "bankst.xls",
    }
    bank_transactions_data = [
        {
            "key": "forbright_bank.pdf",
            "type": "forbright",
            "name": "forbright_bank.pdf",
        },
    ]
    client_id = "a"
    json_body = json.dumps(
        {
            "analysis_name": "test",
            "system_file": system_transactions_data,
            "bank_files": bank_transactions_data,
            "analysis_options": {
                "maxPossibleTransactions": 5,
            },
            "client_id": client_id,
            "analysis_name": "test_analysis",
            "exclusions": {"system": {"test": ["credit card"]}, "bank": {}},
        }
    )
    event = {"Records": [{"body": json_body}]}
    lambda_handler(event, None)
