from typing import Type

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.engine.base import Engine  # type: ignore

from .subscriber_protocol import SubscriberProtocol
from ...db.schemas.word_frequency import WordFrequencyCreate
from ..publishers.word_counter_publisher import FrequencyCounter
from ...db.crud.word_counter import add_word, commit_words


class CounterSubscriber(SubscriberProtocol):
    def __init__(self, engine: Engine, create_schema: Type[WordFrequencyCreate]):
        self.__engine = engine
        self.__create_schema = create_schema
        self.__data: list[FrequencyCounter] = list()

    def add_data(self, data: FrequencyCounter) -> None:
        self.__data.append(data)

    def run(self) -> None:
        if self.__data is None:
            raise ValueError("Data must be set.")

        with Session(self.__engine) as session:
            for frequency_counter_data in self.__data:
                for _ in range(frequency_counter_data.frequency):
                    item_schema = WordFrequencyCreate(word=frequency_counter_data.word)
                    add_word(session, item_schema, commit=False)
            commit_words(session)
