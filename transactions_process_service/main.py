import logging
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from .api.api import api_router



app = FastAPI(
    title="Transactions Process Service",
    description="Process transactions and return the result",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
def startup_event():
    logging.basicConfig(
        filename="app.log",
        filemode="w",
        format="%(asctime)s %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    logging.info("App started")

app.include_router(api_router)


@app.get("/")
async def root():
    return {"info": "OK"}


def start():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
