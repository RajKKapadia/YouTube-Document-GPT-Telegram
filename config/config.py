import os

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

DB_DIR = 'data/db'
OUTPUT_DIR = 'data/output'
