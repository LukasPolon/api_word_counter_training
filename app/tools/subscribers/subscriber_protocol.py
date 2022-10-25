import abc
from typing import Protocol, TypeVar, Type

from ..publishers.word_counter_publisher import FrequencyCounter


class SubscriberProtocol(Protocol):
    @abc.abstractmethod
    def add_data(self, data: FrequencyCounter) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def run(self) -> None:
        raise NotImplementedError
