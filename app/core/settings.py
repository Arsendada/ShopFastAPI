import os
from dotenv import load_dotenv


load_dotenv()


DATABASE_URL: str = os.getenv('DATABASE_URL')
SECRET_KEY: str = os.getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
SMTP_HOST: str = os.getenv('SMTP_HOST')
SMTP_USER: str = os.getenv('SMTP_USER')
SMTP_PASSWORD: str = os.getenv('SMTP_PASSWORD')
SMTP_PORT: str = os.getenv('SMTP_PORT')
EMAILS_ENABLED: bool = False
EMAIL_TEMPLATES_DIR: str = "app/templates"
PROJECT_NAME: str = "shop"
SMTP_TLS: bool = True
SERVER_HOST = 'http://localhost:8000'