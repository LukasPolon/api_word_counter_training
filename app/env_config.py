import os
from typing import Iterator


class EnvConfig:
    def __getitem__(self, key: str) -> str | None:
        return self.get(key)

    def __len__(self) -> int:
        return len(self.items())

    def __iter__(self) -> Iterator:
        return iter(self.items())

    def __contains__(self, item: str) -> bool:
        return item in self.keys()

    def __init__(self) -> None:
        self.__keys: list[str] | None = None
        self.__items: dict[str, str | None] | None = None

    def keys(self) -> list[str]:
        if self.__keys is None:
            self.__keys = [
                "DB_USERNAME",
                "DB_PASSWORD",
                "DB_NAME",
                "DB_HOST",
                "DB_PORT",
                "HTTPD_HOST",
                "HTTPD_PORT",
                "SELF_API_HOST",
                "SELF_API_PORT",
                "SELF_API_LOG_LEVEL",
            ]
        return self.__keys

    def values(self) -> list[str | None]:
        return list(self.items().values())

    def items(self) -> dict[str, str | None]:
        if self.__items is None:
            self.__items = {key: os.getenv(key) for key in self.keys()}

        return self.__items

    def get(self, item: str) -> str | None:
        return self.items()[item]
