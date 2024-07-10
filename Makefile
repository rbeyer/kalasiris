.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

define DOWNLOAD_PYSCRIPT
import urllib.request, sys

urllib.request.urlretrieve(sys.argv[1],sys.argv[2])
endef
export DOWNLOAD_PYSCRIPT


BROWSER := python -c "$$BROWSER_PYSCRIPT"
DOWNLOAD := python -c "$$DOWNLOAD_PYSCRIPT"
DOCSfakeISISROOTbx := docs/fakeISISROOT/bin/xml
ISISXMLS = $(notdir $(wildcard $(ISISROOT)/bin/xml/*) )
fake_isis_progs = $(foreach isisprog, $(ISISXMLS), $(DOCSfakeISISROOTbx)/$(isisprog) )


help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache
	rm -fr test-resources
	rm -fr test-ISIS3DATA

lint/flake8: ## check style with flake8
	flake8 kalasiris tests

lint/black: ## check style with black
	black --check kalasiris tests

lint/ufmt: ## check format with ufmt
	ufmt kalasiris
	ufmt tests

lint: lint/flake8 lint/black lint/ufmt


test: test-resources ## run tests quickly with the default Python
	python -m pytest

test-all: ## run tests on every Python version with tox
	tox

test-ISIS3DATA: ## Download a minimal $ISIS3DATA for testing
	mkdir -p test-ISIS3DATA
	rsync -rltzvR --delete isisdist.astrogeology.usgs.gov::isis3data/data/./base/translations/pdsImage.trn test-ISIS3DATA/
	rsync -rltzvR --delete isisdist.astrogeology.usgs.gov::isis3data/data/./base/templates/labels/CubeFormatTemplate.pft test-ISIS3DATA/
	rsync -rltzvR --delete isisdist.astrogeology.usgs.gov::isis3data/data/./mro/translations/hiriseInstrument.trn test-ISIS3DATA/
	rsync -rltzvR --delete isisdist.astrogeology.usgs.gov::isis3data/data/./mro/translations/hiriseBandBin.trn test-ISIS3DATA/
	rsync -rltzvR --delete isisdist.astrogeology.usgs.gov::isis3data/data/./mro/translations/hiriseArchive.trn test-ISIS3DATA/

test-resources: test-ISIS3DATA ## Download what we need for testing
	mkdir test-resources
	$(DOWNLOAD) https://hirise-pds.lpl.arizona.edu/PDS/EDR/PSP/ORB_010500_010599/PSP_010502_2090/PSP_010502_2090_RED5_0.IMG test-resources/PSP_010502_2090_RED5_0.img

coverage: ## check code coverage quickly with the default Python
	coverage run --source kalasiris -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

fakeISISROOT-docs: ## create a suite of fake ISIS program filenames
	rm -f $(DOCSfakeISISROOTbx)/*
	echo $(ISISXMLS)
	touch $(fake_isis_progs)

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release-check: dist ## check state of distribution
	twine check dist/*

release: dist ## package and upload a release
	twine upload -r kalasiris dist/*

dist: clean ## builds source and wheel package
	python -m build
	ls -l dist

develop: clean  ## install the package in an editable format for development
	pip install --no-deps -e .

install: clean ## install the package to the active Python's site-packages
	pip install
