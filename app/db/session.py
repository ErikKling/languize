from sqlalchemy import Column, Integer, String, Float, Boolean, Date, create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./vocab.db"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()