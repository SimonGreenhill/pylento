.PHONY: build release test clean

PYTHON=./env/bin/python3

build:
	$(PYTHON) setup.py sdist bdist_wheel

release:
	$(PYTHON) setup.py sdist bdist_wheel upload

test: clean
	py.test --cov pylento
	coverage html

clean:
	rm -rf build/*

