from decouple import config

TOKEN = config("BOT_TOKEN")
API_SECRET = config("API_SECRET")
API_URL = config("DJANGO_BASE_URL")
WEB_APP_URL = config("WEB_APP_URL")