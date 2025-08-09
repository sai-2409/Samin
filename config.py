# Keys,Ids,Tokens,etc.

from dotenv import load_dotenv
import os

load_dotenv()  # Загружает переменные из .env

# Теперь просто получаем их из окружения
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

YANDEX_MERCHANT_ID = os.getenv("YANDEX_MERCHANT_ID")
YANDEX_API_URL = os.getenv("YANDEX_API_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
adminPassword = os.getenv("adminPassword")

# Additional API keys
DADATA_API_TOKEN = os.getenv("DADATA_API_TOKEN")
YANDEX_MAPS_API_KEY = os.getenv("YANDEX_MAPS_API_KEY")

# Email configuration
EMAIL_USER = os.getenv("EMAIL_USER", "your-email@yandex.ru")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your-app-password")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@samin.ru")

# Server configuration
DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() == "true"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "5000"))

# Email service configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

# File paths configuration
DATA_DIR = os.getenv("DATA_DIR", "static/data")
PRIVATE_DIR = os.getenv("PRIVATE_DIR", "private")
UPLOADS_DIR = os.getenv("UPLOADS_DIR", "static/uploads")

# File upload configuration
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "5242880"))  # 5MB default
ALLOWED_EXTENSIONS = set(os.getenv("ALLOWED_EXTENSIONS", "png,jpg,jpeg,gif,webp").split(","))

# Application settings
APP_NAME = os.getenv("APP_NAME", "Samin")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
