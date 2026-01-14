import os
from pathlib import Path
from dotenv import load_dotenv


class EnvManager:
    _loaded = False

    @classmethod
    def load(cls, env: str):
        if cls._loaded:
            return

        env_file = Path(f"env/.env.{env}")

        if not env_file.exists():
            raise FileNotFoundError(
                f"Environment file '{env_file}' not found"
            )

        load_dotenv(env_file)
        cls._loaded = True

    @staticmethod
    def get(key: str, required: bool = True) -> str:
        value = os.getenv(key)

        if required and not value:
            raise RuntimeError(f"Missing required env variable: {key}")

        return value
