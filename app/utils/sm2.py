from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Vocabulary
from app.utils.gemini import evaluate_description
from app.services.sm2_logic import update_sm2

router = APIRouter()

@router.post("/evaluate_description/{word_id}")
def evaluate_word_description(word_id: int, description: str, db: Session = Depends(get_db)):
    word = db.query(Vocabulary).filter(Vocabulary.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    response = evaluate_description(description)
    score = response.get("score", 0)
    word.last_score = score

    update_sm2(word, score)
    db.commit()

    return {"word_id": word_id, "score": score}