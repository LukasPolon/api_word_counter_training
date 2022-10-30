import os
import time
import subprocess

import uvicorn
import pytest

from multiprocessing import Process
from dataclasses import dataclass, field

from app.constants import HTTPD_DIR
from app.env_config import EnvConfig


env_config = EnvConfig()


@dataclass
class FileTestMeta:
    words_count: dict[str, int] = field(
        default_factory=lambda: {"one": 4, "two": 3, "three": 2, "four": 1}
    )


@dataclass
class ConfigTest:
    docker_compose_file_path: str = os.path.abspath(
        os.path.join("deployment", "docker-compose.yaml")
    )
    test_file_path: str = os.path.join(HTTPD_DIR, "test_file.txt")
    httpd_url: str = (
        f"http://{env_config.get('HTTPD_HOST')}:{env_config.get('HTTPD_PORT')}"
    )
    test_file_url: str = f"{httpd_url}/test_file.txt"
    api_url: str = (
        f"http://{env_config.get('SELF_API_HOST')}:{env_config.get('SELF_API_PORT')}"
    )


@pytest.fixture()
def reset_database():
    cli = "awct-manage"
    print("Deleting the database")
    subprocess.run([f"{cli}", "db", "delete"])

    print("Creating the database")
    subprocess.run([f"{cli}", "db", "create"])
