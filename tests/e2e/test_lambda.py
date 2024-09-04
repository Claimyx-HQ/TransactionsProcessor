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
            "system_file": system_transactions_data,
            "bank_files": bank_transactions_data,
            "client_id": client_id,
        }
    )
    event = {"Records": [{"body": json_body}]}
    lambda_handler(event, None)
