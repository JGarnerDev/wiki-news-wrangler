import os
from dotenv import load_dotenv
load_dotenv()


SECRET = os.getenv("SECRET")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

DB_RAW_NAME = os.getenv("DB_RAW_NAME")
DB_CLEAN_NAME = os.getenv("DB_CLEAN_NAME")
DB_ANALYTICS_NAME = os.getenv("DB_ANALYTICS_NAME")

HERE_API_KEY = os.getenv("HERE_API_KEY")
