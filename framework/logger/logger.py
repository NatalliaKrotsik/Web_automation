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
        self.logger.setLevel(logging.DEBUG)

        with open(os.path.join(Logger._root_dir, "configs", "logger_config.json")) as f:
            self.config = json.load(f)

        os.makedirs(os.path.join(Logger._root_dir, "logs"), exist_ok=True)

        if Logger._worker_id == "master":
            log_file = os.path.join(Logger._root_dir, "logs", "master.log")
        else:
            log_file = os.path.join(
                Logger._root_dir, "logs", f"worker_{Logger._worker_id}.log"
            )

        handler = logging.FileHandler(log_file, encoding="utf-8")
        handler.setLevel(getattr(logging, self.config.get("level", "INFO").upper()))
        formatter = logging.Formatter(
            self.config.get("format", "{level} [{asctime}] {message}"),
            style="{",
            datefmt="%H:%M:%S",
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        console = logging.StreamHandler()
        console.setLevel(getattr(logging, self.config.get("level", "INFO").upper()))
        console.setFormatter(formatter)
        self.logger.addHandler(console)

        self.step_counter = 0

    @staticmethod
    def log(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = Logger.get_logger().logger
            try:
                result = func(*args, **kwargs)
                return result
            except AssertionError as err:
                logger.error(f"Exception in {func.__name__}: {err}")
                raise
        return wrapper

    @classmethod
    def get_logger(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @staticmethod
    def debug(message: str):
        logger = Logger.get_logger().logger
        logger.debug("*" * 50)
        logger.debug(message)
        logger.debug("*" * 50)

    @staticmethod
    def info(message: str):
        logger = Logger.get_logger().logger
        logger.info(message)

    @staticmethod
    def error(message: str):
        logger = Logger.get_logger().logger
        logger.error(message)
