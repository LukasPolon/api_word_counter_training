from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy import func  # type: ignore

from ..models.word_frequency import WordFrequency as WordFrequencyModel
from ..schemas import word_frequency as word_frequency_schemas


def get_words_by_name(db: Session, word_name: str):
    return (
        db.query(WordFrequencyModel).filter(WordFrequencyModel.word == word_name).all()
    )


def add_word(
    session: Session,
    word_schema: word_frequency_schemas.WordFrequencyCreate,
    commit: bool = True,
) -> WordFrequencyModel:
    word_frequency_row = WordFrequencyModel(
        word=word_schema.word,
    )

    session.add(word_frequency_row)
    if commit:
        session.commit()
        session.refresh(word_frequency_row)
    return word_frequency_row


def commit_words(session: Session) -> None:
    session.commit()
    session.close()


def get_word_count(session: Session, word_name: str) -> int:
    result = (
        session.query(WordFrequencyModel)
        .filter(WordFrequencyModel.word == word_name)
        .count()
    )
    return result
