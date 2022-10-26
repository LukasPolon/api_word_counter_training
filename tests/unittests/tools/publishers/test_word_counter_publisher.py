from unittest import TestCase, mock

from app.tools.publishers.word_counter_publisher import WordCounterPublisher
from app.tools.publishers.word_counter_publisher import FrequencyCounter
from app.tools.subscribers.subscriber_protocol import SubscriberProtocol
from app.tools.chunk_providers.chunk import Chunk


class TestWordCounterPublisher(TestCase):
    def test_run_basic(self):
        """
        Given: initial data and Subscriber added
        When: run() method is executed on tested publisher
        Then: Subscriber is called with FrequencyCounter objects
        """
        mock_subscriber = mock.MagicMock(
            name="mock_subscriber", spec=SubscriberProtocol
        )
        wc_publisher = WordCounterPublisher()
        wc_publisher.add_subscriber(mock_subscriber)

        test_data = Chunk(data="test_data", data_preprocessed=["test", "data"])
        expected_data = [
            mock.call(data=FrequencyCounter(word="data", frequency=1)),
            mock.call(data=FrequencyCounter(word="test", frequency=1)),
        ]
        wc_publisher.add_data(data=test_data)

        wc_publisher.run()

        mock_subscriber.add_data.assert_has_calls(expected_data)
        self.assertTrue(mock_subscriber.run.called)

    def test_run_no_data(self):
        """
        Given: no data added to tested Publisher
        When: run() method is executed on tested publisher
        Then: ValueError is raised
        """
        norm_publisher = WordCounterPublisher()
        with self.assertRaisesRegex(ValueError, "Data must be set"):
            norm_publisher.run()
