ifeq ($(OS), Windows_NT)
	PYTHON = .venv/Scripts/python.exe
	PYTHON_EXE = python3.10.exe
	PIP = .venv/Scripts/pip.exe
	MYPY = .venv/Scripts/mypy.exe
	BLACK = .venv/Scripts/black.exe
	COVERAGE = .venv/Scripts/coverage
	PYTEST = .venv/Scripts/pytest
else
	PYTHON = .venv/bin/python3.10
	PYTHON_EXE = python3.10
	PIP = .venv/bin/pip
	MYPY = .venv/bin/mypy
	BLACK = .venv/bin/black
	COVERAGE = .venv/bin/coverage
	PYTEST = .venv/bin/pytest
endif


install-lints:
	# TODO: Additional packages should have separated requirements file/files
	$(PIP) install black==22.3.0
	$(PIP) install mypy==0.961
	$(PIP) install lxml==4.9.0

install-tests:
	$(PIP) install coverage==6.5.0
	$(PIP) install pytest==7.2.0
	$(PIP) install pytest-dependency==0.5.1

install:
	$(PYTHON_EXE) -m venv .venv
	$(PIP) install -r requirements.txt
	$(PYTHON) setup.py install

install-all: install install-lints install-tests

develop:
	$(PYTHON) setup.py develop

mypy:
	$(MYPY) app/

black:
	$(BLACK) app/ tests/unittests/ tests/functional/

linters: mypy black

clean:
	rm -rf .mypy_cache/
	rm -rf .venv/
	rm -rf build/
	rm -rf dist/
	rm -rf ApiWordCounterTest.egg-info/

unittests:
	$(COVERAGE) run -m pytest tests/unittests
	$(COVERAGE) report

functional-tests:
	$(PYTEST) -v tests/functional/
