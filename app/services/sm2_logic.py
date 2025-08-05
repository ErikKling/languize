

from datetime import date, timedelta

def update_sm2(word, quality: int):
    """
    Updates the vocabulary item using the SM2 algorithm.

    Args:
        word: The vocabulary database model instance.
        quality (int): The quality of the user's response (0–5).
    """
    if quality < 3:
        word.repetition = 0
        word.interval = 1
    else:
        if word.repetition == 0:
            word.interval = 1
        elif word.repetition == 1:
            word.interval = 6
        else:
            word.interval = round(word.interval * word.easiness)

        word.repetition += 1

    # Update easiness factor
    word.easiness = max(1.3, word.easiness + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))

    # Set next review date
    word.next_review = date.today() + timedelta(days=word.interval)

    # Store the last score for transparency
    word.last_score = quality