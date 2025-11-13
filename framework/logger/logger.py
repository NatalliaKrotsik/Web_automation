import functools
import json
import logging
import os
import framework.utils.utils as helpers


class Logger:
    _instance = None
    _worker_id = None
    _root_dir = helpers.get_root_dir()

    def __init__(self):
        self.logger = logging.getLogger("FrameworkLogger")
        self.logger.setLevel(logging.DEBUG)  # default level, can override from config

        with open(os.path.join(Logger._root_dir, "configs", "logger_config.json")) as f:
            self.config = json.load(f)

        # Create log directory if it doesn't exist
        os.makedirs(os.path.join(Logger._root_dir, "logs"), exist_ok=True)

        if Logger._worker_id == "master":
            log_file = os.path.join(Logger._root_dir, "logs", "master.log")
        else:
            log_file = os.path.join(Logger._root_dir, "logs", f"worker_{Logger._worker_id}.log")

        # File handler
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(getattr(logging, self.config.get("level", "INFO").upper()))
        formatter = logging.Formatter(self.config.get("format", "%(asctime)s - %(levelname)s - %(message)s"))
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Optional: also log to console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, self.config.get("level", "INFO").upper()))
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        self.step_counter = 0


    @staticmethod
    def log(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = Logger.get_logger()
            try:
                result = func(*args, **kwargs)
                return result
            except AssertionError as err:
                logger.error(f"Exception in {func.__name__}: {err}")
                raise
        return wrapper

