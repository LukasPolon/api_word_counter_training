from typing import Type, Callable
from dataclasses import dataclass

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.engine.base import Engine  # type: ignore

from ...db.schemas.word_frequency import WordFrequencyCreate
from ..publishers.word_counter_publisher import FrequencyCounter


@dataclass
class CounterSubscriberDatabaseManagement:
    add_word: Callable
    commit_words: Callable


class CounterSubscriber:
    """Collects FrequencyCounter data and saves them in database."""

    def __init__(
        self,
        engine: Engine,
        create_schema: Type[WordFrequencyCreate],
        db_management: CounterSubscriberDatabaseManagement,
    ):
        """CounterSubscriber initializer.

        Args:
            engine: Database Engine object
            create_schema: pydantic schema for Row creation
        """
        self.__engine = engine
        self.__create_schema = create_schema
        self.__db_management = db_management
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
                    self.__db_management.add_word(session, item_schema, commit=False)
            self.__db_management.commit_words(session)
        self.__data = []
