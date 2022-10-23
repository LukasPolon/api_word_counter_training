from typing import Type, Callable

from .publisher_protocol import PublisherProtocol
from ...tools.chunk_providers.chunk import Chunk
from ..subscribers.subscriber_protocol import SubscriberProtocol

from gensim.parsing.preprocessing import preprocess_string  # type: ignore
from gensim.parsing.preprocessing import (
    strip_tags,
    strip_punctuation,
    strip_non_alphanum,
    strip_multiple_whitespaces,
)

from gensim.parsing.preprocessing import split_on_space


class NormalizationPublisher(PublisherProtocol):
    def __init__(self) -> None:
        self.__publishers: list[PublisherProtocol] = []
        self.__subscribers: list[SubscriberProtocol] = []
        self.__data: Chunk | None = None

    def add_data(self, data: Chunk) -> None:
        self.__data = data

    def add_publisher(self, publisher: PublisherProtocol) -> None:
        self.__publishers.append(publisher)

    def add_subscriber(self, subscriber: SubscriberProtocol) -> None:
        self.__subscriber.append(subscriber)

    def run(self) -> None:
        if self.__data is None:
            raise ValueError("Data is not set")
        self.__data.data = preprocess_string(self.__data.data, self.__filters())
        self.__run_publishers(self.__data)

    def __filters(self) -> list[Callable]:
        filters = [
            strip_tags,
            strip_punctuation,
            strip_non_alphanum,
            strip_multiple_whitespaces,
        ]
        return filters

    def __run_publishers(self, data: Chunk) -> None:
        for publisher in self.__publishers:
            publisher.add_data(data=data)
            publisher.run()
