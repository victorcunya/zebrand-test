
from functools import lru_cache
from os import getenv as env

from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    DATABASE_URL: str = env('DATABASE_URL')
    SMTP_SERVER: str = env('SMTP_SERVER')
    SMTP_PORT: str = env('SMTP_PORT')
    SMTP_USERNAME: str = env('SMTP_USERNAME')
    SMTP_PASSWORD: str = env('SMTP_PASSWORD')
    SMTP_USE_TLS: str = env('SMTP_USE_TLS')
    EMAIL_DEFAULT_SENDER: str = env('EMAIL_DEFAULT_SENDER')
    EMAIL_RECIPIENTS: str = env('EMAIL_RECIPIENTS')
    

@lru_cache()
def get_settings():
    return BaseConfig()

settings = get_settings()
