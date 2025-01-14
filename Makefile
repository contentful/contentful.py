.PHONY: clean-pyc clean-build docs clean test lint release

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation"
	@echo "release - package and upload a release"
	@echo "dist - package"

clean: clean-build clean-pyc
	rm -fr htmlcov/

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	pdm run lint

test:
	pdm run test

coverage:
	pdm install -G test
	coverage run --source contentful runtests.py
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	pdm install -G docs
	rm -f docs/contentful.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ contentful
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

release: dist
	pdm publish

dist: clean
	pdm build
