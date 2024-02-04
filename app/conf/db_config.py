"""
    conf/DBConfig.py
"""

import os
from .config import db
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv("./app/.env")
DB_URI = os.environ.get("DB_URI")
DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get('DB_USER')
DB_PORT = os.environ.get('DB_PORT')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_DATABASE = os.environ.get('DB_DATABASE')

class DBConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URL = f'{DB_URI}{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}' 

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    engine = db.create_engine(SQLALCHEMY_DATABASE_URL)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()