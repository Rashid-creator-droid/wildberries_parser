import json

from typing import Optional

from pydantic import TypeAdapter

from core.settings import CONFIG_PATH
from models.main_config import AppConfig


class DataLoader:
    config_path: str = CONFIG_PATH

    def __init__(
        self,
        config_path: Optional[str] = None,
    ):
        self.config_path = config_path or self.config_path

    @staticmethod
    def _read_json(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    def get_config(self) -> AppConfig:
        data = self._read_json(self.config_path)
        return TypeAdapter(AppConfig).validate_python(data)
