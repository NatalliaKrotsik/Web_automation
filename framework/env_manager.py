import yaml
from pathlib import Path
from dotenv import load_dotenv


class EnvManager:
    _loaded = False
    _config: dict = {}

    @classmethod
    def load(cls, env: str):
        if cls._loaded:
            return

        # Load secrets
        env_file = Path(f"env/.env.{env}")
        if env_file.exists():
            load_dotenv(env_file)

        # Load YAML config
        yaml_file = Path(f"configs/{env}.yaml")
        if not yaml_file.exists():
            raise FileNotFoundError(f"Config file '{yaml_file}' not found")

        with open(yaml_file) as f:
            cls._config = yaml.safe_load(f)

        cls._loaded = True

    @classmethod
    def get_config(cls) -> dict:
        return cls._config

    @staticmethod
    def get(key: str, required: bool = True) -> str:
        import os
        value = os.getenv(key)
        if required and not value:
            raise RuntimeError(f"Missing required env variable: {key}")
        return value