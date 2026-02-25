import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
LOGGER_PATH = os.path.join(BASE_DIR, "logs/parser.log")

wb_cookie = os.getenv("WB_COOKIE")
COOKIES = {"x_wbaas_token": wb_cookie}

PROXY_URL = os.getenv("PROXY_URL")

PER_PAGE = 100
SEPARATOR = "=" * 30