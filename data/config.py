from pathlib import Path
from dotenv import dotenv_values


BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / ".env"
BOT_TOKEN = dotenv_values(ENV_PATH)['TOKEN_TG']
SERVER_TOKEN = dotenv_values(ENV_PATH)['TOKEN_ACCESS']
BlOCKCYPHER_TOKEN = dotenv_values(ENV_PATH)['BLOCKCYPHER_TOKEN']
ADDRESS_LTC = dotenv_values(ENV_PATH)['ADDRESS']
PRIV_KEY = dotenv_values(ENV_PATH)['PRIVATE']

admins = [
    1260426275
]

redis = {
    "url": 'redis://redis:6379',
    "encoding": "utf8",
}