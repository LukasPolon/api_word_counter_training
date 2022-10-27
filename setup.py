import sys
from typing import List
from setuptools import setup
from setuptools import find_packages


MIN_PYTHON = (3, 10)
if sys.version_info < MIN_PYTHON:
    sys.exit(
        f"Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} or later is required."
    )


setup(
    name="ApiWordCounterTest",
    author='Lukasz Polon',
    author_email='lukaspolon@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": ["awct-manage = app.manager:manage"]
    },
    data_files=[
        ("deployment", ["deployment/docker-compose.yaml"]),
        ("deployment/httpd", ["deployment/httpd/test_file.txt"])

    ]
)
