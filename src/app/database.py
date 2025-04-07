import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

db_name = "./database/my_db.db"
abs_path = os.path.abspath(db_name)
engine = create_engine(url=f"sqlite:///{abs_path}", echo=False)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db():
    Base.metadata.create_all(engine)
