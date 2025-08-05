from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.db.session import get_db
from app.db.models import Vocabulary
from app.api.schemas import VocabularyOut, EvaluationRequest
from app.utils.gemini import evaluate_description
from app.services.sm2_logic import update_sm2

router = APIRouter()

@router.get("/vocabulary", response_model=List[VocabularyOut])
def fetch_vocabulary(db: Session = Depends(get_db)):
    return db.query(Vocabulary).all()

@router.get("/learn/next", response_model=VocabularyOut)
def get_next_vocabulary(db: Session = Depends(get_db)):
    today = date.today()
    due_word = db.query(Vocabulary).filter(
        Vocabulary.known == False,
        Vocabulary.next_review <= today
    ).order_by(Vocabulary.next_review.asc()).first()

    if due_word:
        return due_word

    new_word = db.query(Vocabulary).filter(
        Vocabulary.known == False,
        Vocabulary.next_review == None
    ).order_by(Vocabulary.id.asc()).first()

    if new_word:
        return new_word

    raise HTTPException(status_code=404, detail="No more words to learn.")

@router.get("/learn/solution/{word_id}", response_model=VocabularyOut)
def get_solution(word_id: int, db: Session = Depends(get_db)):
    word = db.query(Vocabulary).filter_by(id=word_id).first()
    if word is None:
        raise HTTPException(status_code=404, detail="Word not found.")
    return word

@router.post("/evaluate/{word_id}")
def evaluate_word_description(
    word_id: int,
    req: EvaluationRequest,
    db: Session = Depends(get_db)
):
    word = db.query(Vocabulary).filter_by(id=word_id).first()
    if word is None:
        raise HTTPException(status_code=404, detail="Word not found")

    result = evaluate_description(word.word, word.translation, word.example, req.description)
    print("Gemini Evaluation Result:", result)

    word.last_score = result["score"]
    update_sm2(word, word.last_score)
    db.commit()

    return result
