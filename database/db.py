from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()

DATABASE_URL = "sqlite:///shopee_database.sqlite"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_database():
    from .models import OrderData
    Base.metadata.create_all(bind=engine)


def get_session():
    return SessionLocal()

