from typing import Type
from dataclasses import dataclass

from ..publishers.publisher_protocol import PublisherProtocol
from ..chunk_providers.chunk import Chunk

# from ..subscribers.subscriber_protocol import SubscriberProtocol

from gensim import corpora


@dataclass
class FrequencyCounter:
    word: str
    frequency: int


class WordCounterPublisher(PublisherProtocol):
    def __init__(self) -> None:
        self.__publishers: list[PublisherProtocol] = []
        self.__subscribers: list["SubscriberProtocol"] = []
        self.__data: Chunk | None = None

    def add_data(self, data: Chunk) -> None:
        self.__data = data

    def add_publisher(self, publisher: PublisherProtocol) -> None:
        self.__publishers.append(publisher)

    def add_subscriber(self, subscriber: "SubscriberProtocol") -> None:
        self.__subscribers.append(subscriber)

    def run(self) -> None:
        data_dictionary = corpora.Dictionary([self.__data.data])

        # Bag of words: (<word ID>, <frequency count>)
        data_bow: tuple[int, int] = data_dictionary.doc2bow(self.__data.data)

        # Tokens: {<word ID>: <original word>}
        tokens = {token: word for word, token in data_dictionary.token2id.items()}

        # Counter: {<original word>: <frequency count>}
        frequency_counters = [
            FrequencyCounter(word=tokens[word_id], frequency=frequency)
            for word_id, frequency in data_bow
        ]

        for frequency_counter in frequency_counters:
            for subscriber in self.__subscribers:
                subscriber.add_data(data=frequency_counter)
                subscriber.run()
