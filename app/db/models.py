from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Vocabulary(Base):
    __tablename__ = "vocabulary"

    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String, unique=True)
    translation = Column(String)
    example = Column(String)
    
    repetition = Column(Integer, default=0)
    interval = Column(Integer, default=0)
    easiness = Column(Float, default=2.5)
    next_review = Column(Date, nullable=True, default=None)
    known = Column(Boolean, default=False)
    last_score = Column(Integer, default=None)