from unittest import TestCase, mock

from app.tools.publishers.normalization_publisher import NormalizationPublisher
from app.tools.publishers.publisher_protocol import PublisherProtocol
from app.tools.chunk_providers.chunk import Chunk

PUBLISHER_PATH = "app.tools.publishers.normalization_publisher"


class TestNormalizationPublisher(TestCase):
    def test_run_basic(self):
        """
        Given: initial data and  next Publisher added
        When: run() method is executed on tested publisher
        Then: next Publisher is called with preprocessed data
        """
        mock_publisher = mock.MagicMock(name="mock_publisher", spec=PublisherProtocol)

        norm_publisher = NormalizationPublisher()
        test_data = Chunk(data="test_data")
        expected_data = Chunk(data="test_data", data_preprocessed=["test", "data"])

        norm_publisher.add_data(test_data)
        norm_publisher.add_publisher(mock_publisher)
        norm_publisher.run()

        mock_publisher.add_data.assert_called_with(**{"data": expected_data})
        self.assertTrue(mock_publisher.run.called)

    def test_run_no_data(self):
        """
        Given: no data added to tested Publisher
        When: run() method is executed on tested publisher
        Then: ValueError is raised
        """
        norm_publisher = NormalizationPublisher()
        with self.assertRaisesRegex(ValueError, "Data is not set"):
            norm_publisher.run()

    def test_data_filters(self):
        """
        Given: data with characters that needs to be filtered out
        When: run() method is executed on tested publisher
        Then: expected return data
        """

        test_data = [
            {"raw": "one <b> two</b>", "expected": ["one", "two"]},
            {"raw": "three.four", "expected": ["three", "four"]},
            {"raw": "five&&six@", "expected": ["five", "six"]},
            {"raw": "seven    eight\n", "expected": ["seven", "eight"]},
            {"raw": "Nine & Ten", "expected": ["nine", "ten"]},
        ]

        for test_data_variant in test_data:
            mock_publisher = mock.MagicMock(
                name="mock_publisher", spec=PublisherProtocol
            )

            norm_publisher = NormalizationPublisher()
            test_data = Chunk(data=test_data_variant.get("raw"))
            expected_data = Chunk(
                data=test_data_variant.get("raw"),
                data_preprocessed=test_data_variant.get("expected"),
            )

            norm_publisher.add_data(test_data)
            norm_publisher.add_publisher(mock_publisher)
            norm_publisher.run()

            mock_publisher.add_data.assert_called_with(**{"data": expected_data})
            self.assertTrue(mock_publisher.run.called)
