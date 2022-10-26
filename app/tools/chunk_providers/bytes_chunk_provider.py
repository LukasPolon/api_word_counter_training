from .chunk import Chunk


class BytesChunkProvider:
    """Gets a Bytes fragment, decodes and makes it into a list of Chunks.

    A Chunk ends with line separator (\n).
    If last potential Chunk does not end with line separator,
    it becomes a leftovers, which will be used (added to the front)
    by next bytes set (iteration).

    If there are no more data to process, get_final_chunk() must be executed
    to ensure that there are no leftovers left.
    """

    def __init__(self) -> None:
        self.__data: str = ""
        self.__leftovers: str = ""

    def add_data(self, data: bytes) -> None:
        """Decodes given bytes and replaces the attribute."""
        self.__data = data.decode("utf-8")

    def get_chunk(self) -> list[Chunk]:
        """Processes data and produces Chunks."""
        will_be_leftovers = False
        processing_data = f"{self.__leftovers}{self.__data}"
        self.__leftovers = ""

        if not processing_data.endswith("\n"):
            will_be_leftovers = True

        rows = processing_data.split("\n")

        if will_be_leftovers:
            self.__leftovers = rows.pop()

        chunks = [Chunk(data=row) for row in rows if row]

        return chunks

    def get_final_chunk(self) -> Chunk | None:
        """Checks if there are leftovers and makes a Chunk from them."""
        final_chunk = None
        if self.__leftovers:
            final_chunk = Chunk(data=self.__leftovers)
        return final_chunk
