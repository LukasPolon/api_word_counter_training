from unittest import TestCase
from app.tools.chunk_providers.plain_chunk_provider import PlainChunkProvider
from app.tools.chunk_providers.chunk import Chunk


class TestPlainChunkProvider(TestCase):
    def setUp(self) -> None:
        self.__provider = PlainChunkProvider()

    def test_create_single_chunk(self):
        """
        Given: Single data set added to provider
        When: add_data() and get_chunk() are executed
        Then: Chunk instance is returned with correct data
        """
        test_data = "testdata"
        self.__provider.add_data(data=test_data)
        test_chunk = self.__provider.get_chunk()

        self.assertIsInstance(test_chunk, Chunk)
        self.assertEqual(test_chunk.data, test_data)

    def test_create_series_of_chunks(self):
        """
        Given: Two data sets to generate chunks from
        When: add_data() and get_chunk() are executed twice with different data
        Then: each time Chunk instance with correct data is returned
        """
        first_test_data = "firsttestdata"
        second_test_data = "secondtestdata"

        self.__provider.add_data(data=first_test_data)
        first_chunk = self.__provider.get_chunk()

        self.assertIsInstance(first_chunk, Chunk)
        self.assertEqual(first_chunk.data, first_test_data)

        self.__provider.add_data(data=second_test_data)
        second_chunk = self.__provider.get_chunk()

        self.assertIsInstance(second_chunk, Chunk)
        self.assertEqual(second_chunk.data, second_test_data)
