from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.db_config import DbConfig
import pymysql

db_config = DbConfig()
pymysql.install_as_MySQLdb()

SQLALCHEMY_DATABASE_URL = db_config.get_connection_string()
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
