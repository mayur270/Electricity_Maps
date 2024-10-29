"""Config settings/ env variables for the application."""

import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """Base configuration settings."""

    # API_TOKEN = os.getenv('API_TOKEN')
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'DEBUG')
    BASE_URL = os.getenv('BASE_URL', 'https://api.electricitymap.org')
    API_HEADERS = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        # 'auth-token': API_TOKEN,
    }


class DevConfig(BaseConfig):
    """Development configuration settings."""

    pass


config = DevConfig()
