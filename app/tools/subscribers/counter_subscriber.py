from sqlalchemy.orm import Session

from .subscriber_protocol import SubscriberProtocol
from ...db.schemas.word_frequency import WordFrequencyCreate

from ..publishers.word_counter_publisher import FrequencyCounter

from ...db.crud.word_counter import add_word


class CounterSubscriber(SubscriberProtocol):
    def __init__(self, db: Session, create_schema: WordFrequencyCreate):
        self.__db = db
        self.__create_schema = create_schema
        self.__data: FrequencyCounter | None = None

    def add_data(self, data: FrequencyCounter) -> None:
        self.__data = data

    def run(self) -> None:

        for _ in range(self.__data.frequency):
            item_schema = WordFrequencyCreate(word=self.__data.word)
            add_word(self.__db, item_schema)
