from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from redis import Redis

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

redis_client = Redis.from_url(os.getenv("REDIS_URL"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
