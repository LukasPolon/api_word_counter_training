ifeq ($(OS), Windows_NT)
	PYTHON = .venv/Scripts/python.exe
	PYTHON_EXE = python3.10.exe
	PIP = .venv/Scripts/pip.exe
	MYPY = .venv/Scripts/mypy.exe
	BLACK = .venv/Scripts/black.exe
else
	PYTHON = .venv/bin/python3.10
	PYTHON_EXE = python3.10
	PIP = .venv/bin/pip
	MYPY = .venv/bin/mypy
	BLACK = .venv/bin/black
endif


install-lints:
	$(PIP) install black==22.3.0
	$(PIP) install mypy==0.961
	$(PIP) install lxml==4.9.0
	$(MYPY) --install-types --non-interactive

install:
	$(PYTHON_EXE) -m venv .venv
	$(PYTHON) setup.py install

develop:
	$(PYTHON) setup.py develop

mypy:
	$(MYPY) app/

black:
	$(BLACK) app/

linters: mypy black

clean:
	rm -rf .mypy_cache/
	rm -rf .venv/
	rm -rf build/
	rm -rf dist/
	rm -rf ApiWordCounterTest.egg-info/
