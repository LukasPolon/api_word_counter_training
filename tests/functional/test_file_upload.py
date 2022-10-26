import requests

from .conftest import TestConfig, TestFileMeta, reset_database


class TestFileUpload:

    test_config = TestConfig()
    test_file_meta = TestFileMeta()

    def test_file_upload_word_counter_endpoint(self, reset_database):
        files = {"file": open(self.test_config.test_file_path, "rb")}
        word_counter_request = requests.post(
            f"{self.test_config.api_url}/word_counter", files=files
        )
        assert {"Status": "OK"} == word_counter_request.json()
        assert word_counter_request.status_code == 201

    def test_file_upload_with_statistics(self, reset_database):
        files = {"file": open(self.test_config.test_file_path, "rb")}
        word_counter_request = requests.post(
            f"{self.test_config.api_url}/word_counter", files=files
        )
        assert word_counter_request.status_code == 201

        for word, expected_statistics in self.test_file_meta.words_count.items():

            statistics_request = requests.get(
                f"{self.test_config.api_url}/word_statistics/?word={word}"
            )
            assert statistics_request.status_code == 200
            expected_result = {"word": word, "count": expected_statistics}
            assert statistics_request.json() == expected_result

    def test_double_execution_file_upload_with_statistics(self, reset_database):
        for _ in range(2):
            files = {"file": open(self.test_config.test_file_path, "rb")}
            word_counter_request = requests.post(
                f"{self.test_config.api_url}/word_counter", files=files
            )
            assert word_counter_request.status_code == 201

        for word, expected_statistics in self.test_file_meta.words_count.items():

            statistics_request = requests.get(
                f"{self.test_config.api_url}/word_statistics/?word={word}"
            )
            assert statistics_request.status_code == 200
            expected_result = {"word": word, "count": expected_statistics * 2}
            assert statistics_request.json() == expected_result
