import logging.config
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transactions_process_service.config.custom_log_handlers import (
    EmailingTimedRotatingFileHandler,
)
from transactions_process_service.api.api import api_router
from dotenv import load_dotenv


load_dotenv()
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
    log_directory = "logs"
    os.makedirs(log_directory, exist_ok=True)

    logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Create and add the custom handler
    absolute_log_path = os.path.join(base_dir, "logs", "app.log")
    handler = EmailingTimedRotatingFileHandler(
        filename="logs/app.log",
        when="midnight",
        interval=1,
        backupCount=30,
        absolute_path=absolute_log_path,
    )

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(handler)

    logger.info("App started")


app.include_router(api_router)


@app.get("/")
async def root():
    return "Go to /docs for the API documentation"


def start():
    config = uvicorn.Config(app=app, host="0.0.0.0", port=8000, log_level="info", log_config="logging.conf")
    server = uvicorn.Server(config)
    server.run()