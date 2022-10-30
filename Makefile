
install-dev:
	pip install -r requirements-dev.txt

install:
	pip install -r requirements.txt

setup:
	python setup.py install

install-all: install install-dev

develop:
	python setup.py develop

mypy:
	mypy app/

black:
	black app/ tests/unittests/ tests/functional/

linters: mypy black

clean:
	rm -rf .mypy_cache/
	rm -rf .venv/
	rm -rf build/
	rm -rf dist/
	rm -rf ApiWordCounterTest.egg-info/

unittests:
	coverage run -m pytest tests/unittests
	coverage report

functional-tests:
	pytest -v tests/functional/
