from typing import Protocol

from ..publishers import word_counter_publisher as wc_publisher


class SubscriberProtocol(Protocol):
    def add_data(self, data: "wc_publisher.FrequencyCounter") -> None:
        raise NotImplementedError

    def run(self) -> None:
        raise NotImplementedError
