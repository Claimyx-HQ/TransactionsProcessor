from datetime import datetime, UTC
from typing import Dict
from transactions_processor.schemas.analysis_request import (
    AnalysisRequest,
    AnalysisRequestCreate,
)
from transactions_processor.core.config import config
import aiohttp
import asyncio


class AnalysisRequestsService:
    def __init__(self):
        pass

    async def create_request(self, request: AnalysisRequestCreate) -> AnalysisRequest:
        async with aiohttp.ClientSession() as session:
            url = f"{config.analysis_service_url}/v1/analysis/request"
            data = request.dict()
            async with session.post(url, json=data) as response:
                result = await response.json()
                return AnalysisRequest.model_validate(result)

    async def update_request_status(
        self, request_id: str, status: str
    ) -> AnalysisRequest:
        async with aiohttp.ClientSession() as session:
            url = f"{config.analysis_service_url}/v1/analysis/request/{request_id}/status?analysis_status={status}"
            async with session.patch(url) as response:
                result = await response.json()
                return AnalysisRequest.model_validate(result)

    async def complete_request(self, request_id: str, results: Dict) -> AnalysisRequest:
        async with aiohttp.ClientSession() as session:
            end_time = datetime.now(UTC).isoformat()
            url = f"{config.analysis_service_url}/v1/analysis/request/{request_id}/complete"
            async with session.patch(
                url, json={"results": results, "end_time": end_time}
            ) as response:
                update_result = await response.json()
                return AnalysisRequest.model_validate(update_result)

    async def fail_request(self, request_id: str, errors: Dict) -> AnalysisRequest:
        async with aiohttp.ClientSession() as session:
            end_time = datetime.now(UTC).isoformat()
            url = f"{config.analysis_service_url}/v1/analysis/request/{request_id}/fail"
            async with session.patch(
                url, json={"errors": errors, "end_time": end_time}
            ) as response:
                result = await response.json()
                return AnalysisRequest.model_validate(result)
