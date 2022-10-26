from typing import Callable

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


class NormalizationPublisher:
    """Preprocess given data by applying normalization functions."""

    def __init__(self) -> None:
        self.__publishers: list[PublisherProtocol] = []
        self.__subscribers: list[SubscriberProtocol] = []
        self.__data: Chunk | None = None

    def add_data(self, data: Chunk) -> None:
        self.__data = data

    def add_publisher(self, publisher: PublisherProtocol) -> None:
        self.__publishers.append(publisher)

    def add_subscriber(self, subscriber: SubscriberProtocol) -> None:
        self.__subscribers.append(subscriber)

    def run(self) -> None:
        if self.__data is None:
            raise ValueError("Data is not set")
        self.__data.data_preprocessed = preprocess_string(
            self.__data.data, self.__filters()
        )
        self.__run_publishers(self.__data)

    @staticmethod
    def __filters() -> list[Callable]:
        """Normalization functions to be used on data.
        TODO: they may be injected instead of hardcoded if they will need to be configurable

        strip_tags                  : remove tags, e.g. '<b>'
        strip_punctuation           : replace ASCII punctuation (e.g. '.', ',') with spaces
        strip_non_alphanum          : remove non-alphanum, e.g. '&', '^'
        strip_multiple_whitespaces  : remove repeating whitespace characters
                                      and turns tabs and line breaks into spaces
        """
        filters = [
            strip_tags,
            strip_punctuation,
            strip_non_alphanum,
            strip_multiple_whitespaces,
        ]
        return filters

    def __run_publishers(self, data: Chunk) -> None:
        """Executes configured Publishers with preprocessed data.
        Each Publisher gets the same data.
        """
        for publisher in self.__publishers:
            publisher.add_data(data=data)
            publisher.run()
