import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml
from dotenv import load_dotenv


@dataclass
class UIConfig:
    base_url: str
    browser: str
    headless: bool
    slow_mo: int


@dataclass
class APIConfig:
    base_url: str
    timeout: int


@dataclass
class EnvConfig:
    env_name: str
    base_url: str  # shorthand for ui.base_url — used by page objects
    ui: UIConfig
    api: APIConfig


class EnvManager:
    _loaded = False
    _config: Optional[EnvConfig] = None

    @classmethod
    def load(cls, env: str):
        if cls._loaded:
            return

        env_file = Path(f"env/.env.{env}")
        if env_file.exists():
            load_dotenv(env_file)

        yaml_file = Path(f"configs/{env}.yaml")
        if not yaml_file.exists():
            raise FileNotFoundError(f"Config file '{yaml_file}' not found")

        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f)

        ui_data = data.get("ui", {})
        api_data = data.get("api", {})

        ui = UIConfig(
            base_url=ui_data.get("base_url", ""),
            browser=ui_data.get("browser", "chromium"),
            headless=ui_data.get("headless", True),
            slow_mo=ui_data.get("slow_mo", 0),
        )
        api = APIConfig(
            base_url=api_data.get("base_url", ""),
            timeout=api_data.get("timeout", 10),
        )

        cls._config = EnvConfig(
            env_name=data.get("env_name", env),
            base_url=ui.base_url,
            ui=ui,
            api=api,
        )
        cls._loaded = True

    @classmethod
    def get_config(cls) -> EnvConfig:
        if cls._config is None:
            raise RuntimeError("EnvManager not loaded. Call EnvManager.load(env) first.")
        return cls._config

    @staticmethod
    def get(key: str, required: bool = True) -> str:
        value = os.getenv(key)
        if required and not value:
            raise RuntimeError(f"Missing required env variable: {key}")
        return value
