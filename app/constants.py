import os

APP_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.path.join(APP_DIR, ".."))
DEPLOYMENT_DIR = os.path.abspath(os.path.join(BASE_DIR, "deployment"))
HTTPD_DIR = os.path.abspath(os.path.join(DEPLOYMENT_DIR, "httpd"))
TESTS_DIR = os.path.abspath(os.path.join(BASE_DIR, "tests"))
FUNCTIONAL_TESTS_DIR = os.path.abspath(os.path.join(TESTS_DIR, "functional"))
