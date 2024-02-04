from fastapi.security import HTTPBearer
import sqlalchemy
from pathlib import Path
from configparser import ConfigParser

from starlette.config import Config

dir_config = Path('app/conf')


def get_config() -> ConfigParser:
    config = ConfigParser()
    config.read(dir_config / 'config.ini')
    return config


config = Config('.env')

db = sqlalchemy

security = HTTPBearer()