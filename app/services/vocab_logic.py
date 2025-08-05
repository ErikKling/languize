from datetime import date, timedelta
from app.db.models import Vocabulary

def apply_sm2(word: Vocabulary, quality: int) -> Vocabulary:
    if quality < 3:
        word.repetition = 0
        word.interval = 1
    else:
        word.repetition += 1
        if word.repetition == 1:
            word.interval = 1
        elif word.repetition == 2:
            word.interval = 6
        else:
            word.interval = int(word.interval * word.easiness)

        word.easiness += 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
        if word.easiness < 1.3:
            word.easiness = 1.3

    word.next_review = date.today() + timedelta(days=word.interval)
    return word
