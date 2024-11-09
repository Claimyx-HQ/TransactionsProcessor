from datetime import datetime
from typing import Dict, Optional, Any
from beanie import PydanticObjectId
from bson import ObjectId
from pydantic import BaseModel


class AnalysisRequestBase(BaseModel):
    user_id: str
    request_type: str
    parameters: Dict
    status: str
    name: Optional[str] = None


class AnalysisRequestCreate(AnalysisRequestBase):
    pass


class AnalysisRequestUpdate(BaseModel):
    request_type: Optional[str] = None
    parameters: Optional[Dict] = None
    status: Optional[str] = None
    end_time: Optional[datetime] = None
    errors: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None


class AnalysisRequest(AnalysisRequestBase):
    id: PydanticObjectId
    start_time: datetime
    end_time: Optional[datetime] = None
    errors: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
