import os

from .env_config import EnvConfig

env_config = EnvConfig()


APP_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.path.join(APP_DIR, ".."))
DEPLOYMENT_DIR = os.path.abspath(os.path.join(BASE_DIR, "deployment"))
HTTPD_DIR = os.path.abspath(os.path.join(DEPLOYMENT_DIR, "httpd"))
TESTS_DIR = os.path.abspath(os.path.join(BASE_DIR, "tests"))
FUNCTIONAL_TESTS_DIR = os.path.abspath(os.path.join(TESTS_DIR, "functional"))

DATABASE_DATA = {
    "username": env_config.get("DB_USERNAME"),
    "password": env_config.get("DB_PASSWORD"),
    "host": env_config.get("DB_HOST"),
    "port": env_config.get("DB_PORT"),
    "database": env_config.get("DB_NAME"),
}

DATABASE_URL = (
    f"postgresql://{DATABASE_DATA.get('username')}"
    f":{DATABASE_DATA.get('password')}"
    f"@{DATABASE_DATA.get('host')}"
    f":{DATABASE_DATA.get('port')}"
    f"/{DATABASE_DATA.get('database')}"
)
