import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from excursionist.models import Base

load_dotenv()


def create_tables(engine):
    Base.metadata.create_all(engine)


def connect():
    engine = create_engine(os.getenv("DATABASE_URL", "sqlite+pysqlite:///:memory:"))
    return engine


def get_session(engine):
    return sessionmaker(bind=engine)()
