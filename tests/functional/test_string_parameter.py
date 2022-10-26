import requests

from .conftest import TestConfig, TestFileMeta, reset_database


class TestStringParameter:

    test_config = TestConfig()
    test_file_meta = TestFileMeta()

    def test_string_parameter_word_counter_endpoint(self, reset_database):
        word_counter_request = requests.post(
            f"{self.test_config.api_url}/word_counter?string_param='one two, three'"
        )
        assert {"Status": "OK"} == word_counter_request.json()
        assert word_counter_request.status_code == 201

    def test_string_parameter_with_statistics(self, reset_database):
        test_string = "one two,; one"
        expected_stats = {"one": 2, "two": 1}
        word_counter_request = requests.post(
            f"{self.test_config.api_url}/word_counter?string_param='{test_string}'"
        )
        assert word_counter_request.status_code == 201
        for word, expected_statistics in expected_stats.items():
            statistics_request = requests.get(
                f"{self.test_config.api_url}/word_statistics/?word={word}"
            )
            assert statistics_request.status_code == 200
            expected_result = {"word": word, "count": expected_statistics}
            assert statistics_request.json() == expected_result

    def test_double_execution_string_parameter_with_statistics(self, reset_database):
        test_string = "one two,; one"
        expected_stats = {"one": 2, "two": 1}
        for _ in range(2):
            word_counter_request = requests.post(
                f"{self.test_config.api_url}/word_counter?string_param='{test_string}'"
            )
            assert word_counter_request.status_code == 201
        for word, expected_statistics in expected_stats.items():
            statistics_request = requests.get(
                f"{self.test_config.api_url}/word_statistics/?word={word}"
            )
            assert statistics_request.status_code == 200
            expected_result = {"word": word, "count": expected_statistics * 2}
            assert statistics_request.json() == expected_result
