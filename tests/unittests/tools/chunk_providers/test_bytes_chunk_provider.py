from unittest import TestCase

from app.tools.chunk_providers.chunk import Chunk
from app.tools.chunk_providers.bytes_chunk_provider import BytesChunkProvider


class TestBytesChunkProvider(TestCase):
    def setUp(self) -> None:
        self.__provider = BytesChunkProvider()

    def test_get_one_chunk_without_leftovers(self):
        """
        Given: Data with line separator at the end
        When: add_data() and get_chunk are executed
        Then: one Chunk is produced with no leftovers
        """
        test_data = "some data to process\n"
        self.__provider.add_data(data=bytes(test_data, "utf-8"))
        test_chunks = self.__provider.get_chunk()

        self.assertEqual(len(test_chunks), 1)
        self.assertIsInstance(test_chunks[0], Chunk)
        self.assertEqual(test_chunks[0].data, test_data.strip())
        self.assertEqual(self.__provider.get_final_chunk(), None)

    def test_get_multiple_chunks_without_leftovers(self):
        """
        Given: 2x two lines of data, each with separator at the end
        When: add_data() and get_chunk are executed twice
        Then: 2x two chunks are produced, with no leftovers
        """
        test_data_first = "first some data to process\n" "first some data to process\n"
        test_data_second = (
            "second some data to process\n" "second some data to process\n"
        )

        self.__provider.add_data(data=bytes(test_data_first, "utf-8"))
        first_chunks = self.__provider.get_chunk()

        self.assertEqual(len(first_chunks), 2)
        for generated_chunk in first_chunks:
            self.assertEqual(generated_chunk.data, "first some data to process")

        self.__provider.add_data(data=bytes(test_data_second, "utf-8"))
        second_chunks = self.__provider.get_chunk()

        self.assertEqual(len(second_chunks), 2)
        for generated_chunk in second_chunks:
            self.assertEqual(generated_chunk.data, "second some data to process")

        self.assertEqual(self.__provider.get_final_chunk(), None)

    def test_get_one_chunk_with_leftovers(self):
        """
        Given: two pieces of data with no line separators at the end
        When: add_data() and get_chunk() are executed twice
        Then: first and second attempts saves leftovers byt produces no chunks;
              get_final_chunk() provides chunk with all the data
        """
        test_data_first = "some data to process "
        test_data_second = "continue data"

        self.__provider.add_data(bytes(test_data_first, "utf-8"))
        no_chunk = self.__provider.get_chunk()
        self.assertEqual(no_chunk, [])

        self.__provider.add_data(bytes(test_data_second, "utf-8"))
        again_no_chunk = self.__provider.get_chunk()
        self.assertEqual(again_no_chunk, [])

        chunk_from_leftovers = self.__provider.get_final_chunk()
        self.assertIsInstance(chunk_from_leftovers, Chunk)
        self.assertEqual(
            chunk_from_leftovers.data, "some data to process continue data"
        )
