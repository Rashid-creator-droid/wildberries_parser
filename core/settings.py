import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
