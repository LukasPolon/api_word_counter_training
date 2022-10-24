from .chunk_provider_protocol import ChunkProviderProtocol
from .chunk import Chunk


class PlainChunkProvider(ChunkProviderProtocol):
    def __init__(self) -> None:
        self.__data: str = ""

    def add_data(self, data: str) -> None:
        self.__data = data

    def get_chunk(self) -> Chunk:
        chunk = Chunk(data=self.__data)
        return chunk
