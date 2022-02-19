from pathlib import Path
from dotenv import dotenv_values


BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / ".env"
BOT_TOKEN = dotenv_values(ENV_PATH)['TOKEN_TG']

admins = [

]

redis = {
    "url": 'redis://127.0.0.1:6379',
    "encoding": "utf8",
}