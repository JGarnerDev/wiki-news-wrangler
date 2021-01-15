import os
from dotenv import load_dotenv
load_dotenv()


SECRET = os.getenv("SECRET")

DB_RAW_URI = os.getenv("DB_RAW_URI")
DB_CLEAN_URI = os.getenv("DB_CLEAN_URI")
DB_ANALYTICS_URI = os.getenv("DB_ANALYTICS_URI")

HERE_API_KEY = os.getenv("HERE_API_KEY")
