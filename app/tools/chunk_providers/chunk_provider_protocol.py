from typing import Protocol

from .chunk import Chunk


class ChunkProviderProtocol(Protocol):
    def add_data(self, data: str) -> None:
        raise NotImplementedError

    def get_chunk(self) -> Chunk:
        raise NotImplementedError


class BytesChunkProviderProtocol(Protocol):
    def add_data(self, data: bytes) -> None:
        raise NotImplementedError

    def get_chunk(self) -> list[Chunk]:
        raise NotImplementedError

    def get_final_chunk(self) -> Chunk | None:
        raise NotImplementedError()
