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
BASH_PATH:=/usr/bin/bash
endif
# macOS
ifneq (,$(findstring Darwin, $(UNAME)))
_OS:=macos
BASH_PATH:=$(shell which bash)
endif
# Linux
ifneq (,$(findstring Linux, $(UNAME)))
_OS:=linux
BASH_PATH:=$(shell which bash)
endif
# --- OS Settings --- END --------------------------------------------------------------

VENV_DIR_PATH:=${ROOT_DIR}/.VENV
REQUIREMENTS_FILE_PATH:=${ROOT_DIR}/requirements.txt

SHELL:=${BASH_PATH}

ifneq (,$(findstring venv-,${MAKECMDGOALS}))
ifneq ("$(wildcard ${VENV_DIR_PATH}/bin/activate)","")
SHELL:=. ${VENV_DIR_PATH}/bin/activate && ${SHELL}
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


# --- VENV --- START ------------------------------------------------------------
## 
##VENV
##----
venv-prepare: ## Create a Python virtual environment with venv
	python -m venv ${VENV_DIR_PATH} && \
	python -m pip install -U setuptools pip wheel

venv-install: ## Install Python packages
## Provide PACKAGE_NAME=<package_name> to install a specific package
## Example: make venv-install PACKAGE_NAME=requests
	pip install -r ${REQUIREMENTS_FILE_PATH} ${PACKAGE_NAME}

venv-requirements-update: ## Update requirements.txt with current packages
	pip freeze > ${REQUIREMENTS_FILE_PATH} && \
	cat ${REQUIREMENTS_FILE_PATH}

venv-freeze: ## List installed packages
	pip freeze
# --- VENV --- END --------------------------------------------------------------
