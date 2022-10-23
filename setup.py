import sys
from typing import List
from setuptools import setup
from setuptools import find_packages


MIN_PYTHON = (3, 10)
if sys.version_info < MIN_PYTHON:
    sys.exit(
        f"Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} or later is required."
    )

def get_requirements() -> List[str]:
    """ Get all Python modules required by application to be installed.
        Returns:
            modules: list of Python libs to install
    """
    requirements_file_path = "requirements.txt"
    with open(requirements_file_path, "r", encoding="UTF-8") as req_file:
        modules = req_file.readlines()
    modules = [module.strip() for module in modules if module]
    return modules


setup(
    name="ApiWordCounterTest",
    install_requires=get_requirements(),
    author='Lukasz Polon',
    author_email='lukaspolon@gmail.com',
    packages=find_packages()
)
