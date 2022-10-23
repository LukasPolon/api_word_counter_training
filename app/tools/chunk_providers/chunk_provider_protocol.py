import abc
from typing import Protocol
from dataclasses import dataclass

from .chunk import Chunk


class ChunkProviderProtocol(Protocol):
    """<fill>"""

    @abc.abstractmethod
    def add_data(self, data: bytes) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_chunk(self) -> list[Chunk]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_final_chunk(self) -> Chunk | None:
        raise NotImplementedError()
