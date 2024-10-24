import json
import pathlib
import os
from typing import List, Tuple, Type
from pydantic import BaseModel, Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class AppConifg(BaseSettings):
    analysis_service_url: str = Field(..., env="ANALYSIS_SERVICE_URL")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = AppConifg()
