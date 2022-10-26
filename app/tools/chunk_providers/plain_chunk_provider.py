from .chunk_provider_protocol import ChunkProviderProtocol
from .chunk import Chunk


class PlainChunkProvider:
    """Gets a single piece of data and transforms it into a Chunk."""

    def __init__(self) -> None:
        self.__data: str = ""

    def add_data(self, data: str) -> None:
        """Replaces current data attribute.

        Args:
            data: a string to transform into a Chunk
        """
        self.__data = data

    def get_chunk(self) -> Chunk:
        """Gets stored data and returns a Chunk from it."""
        chunk = Chunk(data=self.__data)
        return chunk
