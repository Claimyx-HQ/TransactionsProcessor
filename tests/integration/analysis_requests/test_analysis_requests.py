from transactions_processor.data.requests_repository import RequestsRepository
from transactions_processor.schemas.analysis_request import (
    AnalysisRequest,
    AnalysisRequestCreate,
)
from transactions_processor.services.analysis_requests_service import (
    AnalysisRequestsService,
)


async def test_add_request():
    analysis_requets_service = AnalysisRequestsService()
    analysis_request_create = AnalysisRequestCreate(
        user_id="1",
        request_type="reconciliation",
        parameters={
            "system_file": {
                "key": "bankst.xls",
                "type": "ncs",
                "name": "bankst.xls",
            },
            "bank_files": [
                {
                    "key": "forbright_bank.pdf",
                    "type": "forbright",
                    "name": "forbright_bank.pdf",
                },
            ],
            "client_id": "a",
        },
        status="processing",
    )
    analysis_request = await analysis_requets_service.create_request(
        analysis_request_create
    )
    new_status = "in_progress"
    await analysis_requets_service.update_request_status(
        str(analysis_request.id), new_status  # type: ignore
    )
    results = {
        "transactions": {
            "total_transactions": 10,
            "matched_transactions": 5,
            "unmatched_transactions": 5,
        },
    }
    await analysis_requets_service.complete_request(str(analysis_request.id), results)
