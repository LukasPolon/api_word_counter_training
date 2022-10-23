from sqlalchemy.orm import Session

from ..models.word_frequency import WordFrequency as WordFrequencyModel
from ..schemas import word_frequency as word_frequency_schemas


def get_words_by_name(db: Session, word_name: str):
    return (
        db.query(WordFrequencyModel).filter(WordFrequencyModel.word == word_name).all()
    )


def add_word(db: Session, word_schema: word_frequency_schemas.WordFrequencyCreate):
    word_frequency_row = WordFrequencyModel(
        word=word_schema.word,
    )
    db.add(word_frequency_row)
    db.commit()
    db.refresh(word_frequency_row)
    return word_frequency_row
