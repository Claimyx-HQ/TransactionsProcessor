from typing import Any, List
from typing import Annotated

from fastapi import APIRouter, Depends, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse


router = APIRouter()
some_file_path = "README.md"


@router.post(
    "/process",
    # response_model=List[BuyBoxData],
)
async def process_transactions(
    system_file: Annotated[bytes, File()], bank_file: Annotated[bytes, File()]
):
    return FileResponse(some_file_path)


@router.get(
    "/mewo",
    # response_model=List[BuyBoxData],
)
async def meow():
    return FileResponse(some_file_path)
