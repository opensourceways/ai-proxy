import json
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import root_validator
from typing import Dict

BASE_DIR = Path.cwd()

class Settings(BaseSettings):
    """Application settings."""
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Keep MODEL_PORT as a string type (it will be a JSON string)
    MODEL_PORT: str = '{"Qwen2.5-32B-Instruct": 8008, "Qwen2.5-14B-Instruct": 8009, "bge-large-en-v1.5": 8010}'
    PORT_DICT: Dict[str, int] = {}
    class Config:
        env_file = f"{BASE_DIR}/.env"
        env_file_encoding = "utf-8"
    # Parsing the MODEL_PORT string as a dictionary
    @root_validator(pre=True)
    def parse_port_dict(cls, values):
        model_port_str = values.get("MODEL_PORT", "{}")
        try:
            # Make sure the string is parsed into a dictionary
            values["PORT_DICT"] = json.loads(model_port_str)
        except json.JSONDecodeError:
            raise ValueError("MODEL_PORT must be a valid JSON string")

        return values


# Example usage
settings = Settings()
print("port: {settings.PORT_DICT}")
