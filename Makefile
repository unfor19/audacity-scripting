#!make
.ONESHELL:
.EXPORT_ALL_VARIABLES:
.PHONY: all $(MAKECMDGOALS)


UNAME := $(shell uname)
ROOT_DIR:=${CURDIR}


# --- OS Settings --- START ------------------------------------------------------------
# Windows
ifneq (,$(findstring NT, $(UNAME)))
_OS:=windows
endif
# macOS
ifneq (,$(findstring Darwin, $(UNAME)))
_OS:=macos
AUDACITY_BIN_PATH:=/Applications/Audacity.app/Contents/MacOS/Wrapper
endif
# Linux
ifneq (,$(findstring Linux, $(UNAME)))
_OS:=linux
endif
# --- OS Settings --- END --------------------------------------------------------------

VENV_DIR_PATH:=${ROOT_DIR}/.VENV
REQUIREMENTS_FILE_PATH:=${ROOT_DIR}/requirements.txt

SHELL:=bash

ifneq (,$(findstring venv-,${MAKECMDGOALS}))
ifneq (,$(wildcard ${VENV_DIR_PATH}/bin/activate))
SHELL:=. ${VENV_DIR_PATH}/bin/activate && bash
endif
endif

# Removes blank rows - fgrep -v fgrep
# Replace ":" with "" (nothing)
# Print a beautiful table with column
help: ## Print this menu
	@echo
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's~:.* #~~' | column -t -s'#'
	@echo
usage: help


# To validate env vars, add "validate-MY_ENV_VAR"
# as a prerequisite to the relevant target/step
validate-%:
	@if [[ -z '${${*}}' ]]; then \
		echo 'ERROR: Environment variable $* not set' && \
		exit 1 ; \
	fi


# --- Audacity --- START ------------------------------------------------------------
##
##AUDACITY
##--------
audacity-start: ## Start Audacity GUI app
	@echo Starting Audacity
	@${AUDACITY_BIN_PATH} &
# --- Audacity --- END --------------------------------------------------------------



# --- VENV --- START ------------------------------------------------------------
## 
##VENV
##----
venv-prepare: ## Create a Python virtual environment with venv
	python -m venv ${VENV_DIR_PATH} && \
	python -m pip install -U setuptools pip wheel && \
	ls ${VENV_DIR_PATH}

venv-install: ## Install Python packages
## Provide PACKAGE_NAME=<package_name> to install a specific package
## Example: make venv-install PACKAGE_NAME=requests
	if [[ -f "${REQUIREMENTS_FILE_PATH}" ]]; then \
		pip install -r ${REQUIREMENTS_FILE_PATH} ${PACKAGE_NAME} ; \
	elif [[ -n "${PACKAGE_NAME}" ]]; then \
		pip install ${PACKAGE_NAME} ; \
	else \
		echo "ERROR: No requirements.txt file found and no package name provided" ; \
		exit 1 ; \
	fi

venv-install-edit: ## Install CLI in editable mode
	pip install -e .

venv-requirements-update: ## Update requirements.txt with current packages
	pip freeze | grep -v '\-e' > ${REQUIREMENTS_FILE_PATH} && \
	cat ${REQUIREMENTS_FILE_PATH}

venv-freeze: ## List installed packages
	pip freeze

venv-run: audacity-start ## Run main app script
	@python main.py

venv-test: audacity-start ## Run tests
	python -m unittest discover -s tests -p 'test_*.py'

venv-test-clean:
	rm -f ${ROOT_DIR}/tests/data/*.trimmed.*
# --- VENV --- END --------------------------------------------------------------
