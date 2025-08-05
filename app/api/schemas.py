from pydantic import BaseModel
from datetime import date
from typing import Optional

class VocabularyOut(BaseModel):
    id: int
    word: str
    translation: Optional[str] = None
    example: str
    repetition: int
    interval: int
    easiness: float
    next_review: date | None
    known: bool
    last_score: Optional[int] = None

    class Config:
        from_attributes = True

class ScoreIn(BaseModel):
    score: int

class EvaluationRequest(BaseModel):
    description: str