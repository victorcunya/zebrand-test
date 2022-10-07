
from functools import lru_cache
from os import getenv as env

from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    DATABASE_URL: str = env('DATABASE_URL')
    

@lru_cache()
def get_settings():
    return BaseConfig()

settings = get_settings()
