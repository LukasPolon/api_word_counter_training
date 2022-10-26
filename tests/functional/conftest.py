import os
import time
import subprocess

import uvicorn
import pytest

from multiprocessing import Process
from dataclasses import dataclass, field

from app.constants import HTTPD_DIR


@dataclass
class TestFileMeta:
    words_count: dict[str, int] = field(
        default_factory=lambda: {"one": 4, "two": 3, "three": 2, "four": 1}
    )


@dataclass
class TestConfig:
    docker_compose_file_path: str = os.path.abspath(
        os.path.join("deployment", "docker-compose.yaml")
    )
    test_file_path: str = os.path.join(HTTPD_DIR, "test_file.txt")
    api_url: str = "http://127.0.0.1:8000"
    test_file_url: str = "http://127.0.0.1:8080/test_file.txt"


@pytest.fixture(scope="session", autouse=True)
def docker_compose_up():
    print("Starting docker-compose")
    config = TestConfig()
    up_result = subprocess.run(
        ["docker-compose", "-f", f"{config.docker_compose_file_path}", "up", "-d"],
        shell=True,
        text=True,
    )
    assert up_result.returncode == 0
    time.sleep(
        15
    )  # would be better to use Docker API to wait for the database to setup

    yield

    print("Stopping docker-compose")
    config = TestConfig()
    stop_result = subprocess.run(
        ["docker-compose", "-f", f"{config.docker_compose_file_path}", "stop"],
        shell=True,
        text=True,
    )
    assert stop_result.returncode == 0


def run():
    uvicorn.run("app.main:app", port=8000, log_level="critical")


@pytest.fixture(scope="session", autouse=True)
def run_api():
    print("Starting API")
    uvicorn_process = Process(target=run, args=(), daemon=True)
    uvicorn_process.start()
    time.sleep(15)  # it would be better to wait for actual start
    yield
    print("Killing API")
    uvicorn_process.kill()


@pytest.fixture()
def reset_database():
    cli = "awct-manage"
    if os.name == "nt":
        cli = "awct-manage.exe"

    print("Deleting the database")
    subprocess.run([f"{cli}", "db", "delete"])

    print("Creating the database")
    subprocess.run([f"{cli}", "db", "create"])
