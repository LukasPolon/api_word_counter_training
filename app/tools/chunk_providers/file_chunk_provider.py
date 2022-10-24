from .chunk_provider_protocol import FileChunkProviderProtocol
from .chunk import Chunk


class FileChunkProvider(FileChunkProviderProtocol):
    def __init__(self) -> None:
        self.__data: str = ""
        self.__leftovers: str = ""

    def add_data(self, data: bytes) -> None:
        self.__data = data.decode("utf-8")

    def get_chunk(self) -> list[Chunk]:
        will_be_leftowers = False
        processing_data = f"{self.__leftovers}{self.__data}"
        self.__leftovers = ""

        if not processing_data.endswith("\n"):
            will_be_leftowers = True

        rows = processing_data.split("\n")

        if will_be_leftowers:
            self.__leftovers = rows.pop()

        chunks = [Chunk(data=row) for row in rows if row]

        return chunks

    def get_final_chunk(self) -> Chunk | None:
        final_chunk = None

        if self.__leftovers:
            final_chunk = Chunk(data=self.__leftovers)
        return final_chunk
