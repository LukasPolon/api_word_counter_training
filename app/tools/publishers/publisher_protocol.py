import abc
from typing import Protocol, TypeVar, Type

from app.tools.chunk_providers.chunk import Chunk

# from ..subscribers.subscriber_protocol import SubscriberProtocol


TPublisherProtocol = TypeVar("TPublisherProtocol", bound="PublisherProtocol")


class PublisherProtocol(Protocol):
    @abc.abstractmethod
    def add_data(self, data: Chunk) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def add_publisher(self, publisher: TPublisherProtocol) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def add_subscriber(self, subscriber) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def run(self) -> None:
        raise NotImplementedError
