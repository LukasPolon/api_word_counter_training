import os

APP_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.path.join(APP_DIR, ".."))
DEPLOYMENT_DIR = os.path.abspath(os.path.join(BASE_DIR, "deployment"))
HTTPD_DIR = os.path.abspath(os.path.join(DEPLOYMENT_DIR, "httpd"))
TESTS_DIR = os.path.abspath(os.path.join(BASE_DIR, "tests"))
FUNCTIONAL_TESTS_DIR = os.path.abspath(os.path.join(TESTS_DIR, "functional"))

DATABASE_DATA = {
    "username": "test",
    "password": "test",
    "host": "127.0.0.1",
    "port": "5432",
    "database": "test"
}
DATABASE_URL = (
    f"postgresql://{DATABASE_DATA.get('username')}"
    f":{DATABASE_DATA.get('password')}"
    f"@{DATABASE_DATA.get('host')}"
    f":{DATABASE_DATA.get('port')}"
    f"/{DATABASE_DATA.get('database')}"
)

