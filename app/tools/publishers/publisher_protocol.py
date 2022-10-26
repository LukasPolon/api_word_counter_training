from typing import Protocol, TypeVar

from app.tools.chunk_providers.chunk import Chunk

from ..subscribers import subscriber_protocol as sub_protocol


TPublisherProtocol = TypeVar("TPublisherProtocol", bound="PublisherProtocol")


class PublisherProtocol(Protocol):
    def add_data(self, data: Chunk) -> None:
        raise NotImplementedError

    def add_publisher(self, publisher: TPublisherProtocol) -> None:
        raise NotImplementedError

    def add_subscriber(self, subscriber: "sub_protocol.SubscriberProtocol") -> None:
        raise NotImplementedError()

    def run(self) -> None:
        raise NotImplementedError
