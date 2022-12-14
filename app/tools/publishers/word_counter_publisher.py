from dataclasses import dataclass

from ..publishers import publisher_protocol as publisher_p
from ..subscribers import subscriber_protocol as sub_p
from ..chunk_providers.chunk import Chunk

from gensim import corpora  # type: ignore


@dataclass(slots=True)
class FrequencyCounter:
    word: str
    frequency: int


class WordCounterPublisher:
    """USes Gensim and Bag of Words feature to count the words."""

    def __init__(self) -> None:
        self.__publishers: list["publisher_p.PublisherProtocol"] = []
        self.__subscribers: list["sub_p.SubscriberProtocol"] = []
        self.__data: Chunk | None = None

    def add_data(self, data: Chunk) -> None:
        self.__data = data

    def add_publisher(self, publisher: "publisher_p.PublisherProtocol") -> None:
        self.__publishers.append(publisher)

    def add_subscriber(self, subscriber: "sub_p.SubscriberProtocol") -> None:
        self.__subscribers.append(subscriber)

    def run(self) -> None:
        if self.__data is None or self.__data.data_preprocessed is None:
            raise ValueError("Data must be set")

        data_dictionary = corpora.Dictionary([self.__data.data_preprocessed])

        # Bag of words: (<word ID>, <frequency count>)
        data_bow = data_dictionary.doc2bow(self.__data.data_preprocessed)

        # Tokens: {<word ID>: <original word>}
        tokens = {token: word for word, token in data_dictionary.token2id.items()}

        # Counter: {<original word>: <frequency count>}
        frequency_counters = [
            FrequencyCounter(word=tokens[word_id], frequency=frequency)
            for word_id, frequency in data_bow
        ]
        self.__run_subscribers(frequency_counters)

    def __run_subscribers(self, counters: list[FrequencyCounter]) -> None:
        for frequency_counter in counters:
            for subscriber in self.__subscribers:
                subscriber.add_data(data=frequency_counter)

        for subscriber in self.__subscribers:
            subscriber.run()
