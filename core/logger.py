import logging
import os
from contextlib import contextmanager

from core.settings import LOGGER_PATH, SEPARATOR

os.makedirs(os.path.dirname(LOGGER_PATH), exist_ok=True)


class Logger:
    _logger = None
    _name = "API_test_logger"
    _indent_level = 0
    _indent_str = "    "

    @classmethod
    def _init_logger(cls):
        cls._logger = logging.getLogger(cls._name)
        cls._logger.propagate = False

        if not cls._logger.handlers:
            cls._logger.setLevel(logging.DEBUG)

            file_handler = logging.FileHandler(LOGGER_PATH, mode="a", encoding="utf-8")
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )
            cls._logger.addHandler(file_handler)

    @classmethod
    def _log(cls, level_method, msg):
        indent = cls._indent_str * cls._indent_level
        level_method(f"{indent}{msg}")

    @classmethod
    def get_logger(cls):
        if cls._logger is None:
            cls._init_logger()
        return cls._logger

    @classmethod
    def info(cls, msg):
        cls._log(cls.get_logger().info, msg)

    @classmethod
    def debug(cls, msg):
        cls._log(cls.get_logger().debug, msg)

    @classmethod
    def warning(cls, msg):
        cls._log(cls.get_logger().warning, msg)

    @classmethod
    def error(cls, msg):
        cls._log(cls.get_logger().error, msg)

    @staticmethod
    def log_clean_line(message=""):
        with open(LOGGER_PATH, "a", encoding="utf-8") as f:
            f.write(SEPARATOR + message + SEPARATOR + "\n\n")

    @classmethod
    def delete_log(cls):
        with open(LOGGER_PATH, "w", encoding="utf-8"):
            pass

    @classmethod
    @contextmanager
    def step(cls, description):
        cls._log(cls.get_logger().info, f"=== STEP START: {description} ===")
        cls._indent_level += 1
        try:
            yield
        except Exception:
            cls._log(cls.get_logger().error, f"=== STEP FAILED: {description} ===")
            raise
        finally:
            cls._indent_level -= 1
            if cls._indent_level < 0:
                cls._indent_level = 0
            cls._log(cls.get_logger().info, f"=== STEP END: {description} ===")
            with open(LOGGER_PATH, "a", encoding="utf-8") as f:
                f.write("\n\n")