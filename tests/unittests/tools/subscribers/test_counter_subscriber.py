from unittest import TestCase, mock

from app.tools.subscribers.counter_subscriber import CounterSubscriber
from app.tools.publishers.word_counter_publisher import FrequencyCounter

SUBSCRIBER_PATH = "app.tools.subscribers.counter_subscriber"


class TestCounterSubscriber(TestCase):
    """TODO: needs tests which will check adding multiple words with multiple frequencies"""

    @mock.patch(f"{SUBSCRIBER_PATH}.commit_words")
    @mock.patch(f"{SUBSCRIBER_PATH}.add_word")
    @mock.patch(f"{SUBSCRIBER_PATH}.Session")
    def test_run_base(self, mock_session, mock_add_word, mock_commit_words):
        """
        Given: mocked arguments and data provided
        When: run() method is called
        Then: session is created, word is added once, commit is invoked once
        """
        mock_engine = mock.MagicMock(name="mock_engine")
        mock_create_schema = mock.MagicMock(name="mock_create_schema")

        counter_subscriber = CounterSubscriber(
            engine=mock_engine, create_schema=mock_create_schema
        )

        test_data = FrequencyCounter(word="test", frequency=1)

        counter_subscriber.add_data(test_data)
        counter_subscriber.run()

        mock_create_schema.assert_called_with(word="test")
        mock_session.assert_called_with(mock_engine)
        mock_add_word.assert_called_with(
            mock_session().__enter__(), mock_create_schema(), commit=False
        )
        mock_commit_words.assert_called_with(mock_session().__enter__())
