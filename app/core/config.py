import os
import multiprocessing
from pydantic_settings import BaseSettings

PORT = int(os.environ.get("PORT", 8080))
DEBUG_MODE = int(os.environ.get("DEBUG_MODE", 1))

# Gunicorn config
bind = ":" + str(PORT)
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2 * multiprocessing.cpu_count()
fast_api = True
listen = "0.0.0.0"

class Configs(BaseSettings):
    PROJECT_NAME: str = "Enjoy2gether-dev"
    API: str = "/api"
    API_V1_STR: str = "/api/v1"
    API_V2_STR: str = "/api/v2"

    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # date
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"



configs = Configs()