from typing import Type

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.engine.base import Engine  # type: ignore

from ...db.schemas.word_frequency import WordFrequencyCreate
from ..publishers.word_counter_publisher import FrequencyCounter
from ...db.crud.word_counter import (
    add_word,
    commit_words,
)  # TODO: those functions should be injected


class CounterSubscriber:
    """Collects FrequencyCounter data and saves them in database."""

    def __init__(self, engine: Engine, create_schema: Type[WordFrequencyCreate]):
        """CounterSubscriber initializer.

        Args:
            engine: Database Engine object
            create_schema: pydantic schema for Row creation
        """
        self.__engine = engine
        self.__create_schema = create_schema
        self.__data: list[FrequencyCounter] = list()

    def add_data(self, data: FrequencyCounter) -> None:
        """Stores Frequency data without override."""
        self.__data.append(data)

    def run(self) -> None:
        """Creates database session, adds objects to the transaction,
        and then commits all objects to database.

        Creates number of rows equal to frequency of the word.
        """
        with Session(self.__engine) as session:
            for frequency_counter_data in self.__data:
                for _ in range(frequency_counter_data.frequency):
                    item_schema = self.__create_schema(word=frequency_counter_data.word)
                    add_word(session, item_schema, commit=False)
            commit_words(session)
        self.__data = []
