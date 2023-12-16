#!make
.ONESHELL:
.EXPORT_ALL_VARIABLES:
.PHONY: all $(MAKECMDGOALS)


UNAME := $(shell uname)
ROOT_DIR:=${CURDIR}
BASH_PATH:=$(shell which bash)

VENV_DIR_PATH:=${ROOT_DIR}/.VENV
REQUIREMENTS_FILE_PATH:=${ROOT_DIR}/requirements.txt
AUDACITY_SRC_CONFIG_PATH:=${ROOT_DIR}/audacity.cfg

# --- OS Settings --- START ------------------------------------------------------------
# Windows
ifneq (,$(findstring NT, $(UNAME)))
_OS:=windows
VENV_BIN_ACTIVATE:=${VENV_DIR_PATH}/Scripts/activate.bat
AUDACITY_BIN_PATH:="C:\Program Files\Audacity\audacity.exe"
AUDACITY_PREFERENCES_PATH:=${APPDATA}/audacity/audacity.cfg
AUDACITY_KILL_COMMAND:=powershell -c "taskkill /F /IM Audacity.exe /T"

# TODO: Set it - currently getting it from GitHub Actions on Windows
ifeq (${CI},true)
AUDACITY_PREFERENCES_PATH:=/C/Users/runneradmin/AppData/Roaming/audacity/audacity.cfg
endif

endif
# macOS
ifneq (,$(findstring Darwin, $(UNAME)))
_OS:=macos
AUDACITY_BIN_PATH:=/Applications/Audacity.app/Contents/MacOS/Wrapper
AUDACITY_PREFERENCES_PATH:=${HOME}//Library/Application Support/audacity/audacity.cfg
AUDACITY_KILL_COMMAND:=killall Audacity
VENV_BIN_ACTIVATE:=${VENV_DIR_PATH}/bin/activate
endif
# --- OS Settings --- END --------------------------------------------------------------

SHELL:=${BASH_PATH}

ifneq (,$(findstring venv-,${MAKECMDGOALS}))
ifneq (,$(wildcard ${VENV_BIN_ACTIVATE}))


ifeq (${_OS},macos)
SHELL:=source .VENV/bin/activate && ${SHELL}
endif
ifeq (${_OS},windows)
SHELL:=${VENV_BIN_ACTIVATE} && ${SHELL}
endif


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

print-vars:
	@echo "AUDACITY_SRC_CONFIG_PATH=${AUDACITY_SRC_CONFIG_PATH}"
	@echo "AUDACITY_BIN_PATH=${AUDACITY_BIN_PATH}"
	@echo "VENV_BIN_ACTIVATE=${VENV_BIN_ACTIVATE}"
	@echo "REQUIREMENTS_FILE_PATH=${REQUIREMENTS_FILE_PATH}"
	@echo "VENV_DIR_PATH=${VENV_DIR_PATH}"
	@echo "CI=${CI}"

# --- Audacity --- START ------------------------------------------------------------
##
##AUDACITY
##--------
audacity-update-config:
	@if [[ -f "${AUDACITY_PREFERENCES_PATH}" ]]; then \
		echo "Updating ${AUDACITY_PREFERENCES_PATH} file" ; \
		sed -i.bak 's/mod-script-pipe=4/mod-script-pipe=1/' "${AUDACITY_PREFERENCES_PATH}" ; \
		sed -i.bak 's/UpdateNoticeShown=0/UpdateNoticeShown=1/' "${AUDACITY_PREFERENCES_PATH}" ; \
		cat "${AUDACITY_PREFERENCES_PATH}" ; \
		grep 'mod-script-pipe=1' "${AUDACITY_PREFERENCES_PATH}" ; \
	else \
		echo "ERROR: ${AUDACITY_PREFERENCES_PATH} file not found" ; \
		exit 1 ; \
	fi

audacity-print-config:
	@if [[ -f "${AUDACITY_PREFERENCES_PATH}" ]]; then \
		cat "${AUDACITY_PREFERENCES_PATH}" ; \
	else \
		echo "ERROR: ${AUDACITY_PREFERENCES_PATH} file not found" ; \
		exit 1 ; \
	fi

audacity-start: ## Start Audacity GUI app
	@echo Starting Audacity ...
	@${AUDACITY_BIN_PATH} &
	@if [[ "${_CI}" = "true" ]]; then \
		echo "Sleeping 10 seconds to allow Audacity to start the pipes ..." ; \
		sleep 10 ; \
		echo "Hopefully Audacity is up" ; \
	fi

audacity-test-pipe:
	@if [[ "${_OS}" = "windows" ]]; then \
		pipelist ; \
		pipelist | grep SrvPipe ; \
	fi
	python ${ROOT_DIR}/scripts/audacity_pipetest.py

audacity-kill:
	${AUDACITY_KILL_COMMAND}

audacity-restart: audacity-kill audacity-start
	
# --- Audacity --- END --------------------------------------------------------------


# --- VENV --- START ------------------------------------------------------------
## 
##VENV
##----
venv-prepare: ## Create a Python virtual environment with venv
	python -m venv ${VENV_DIR_PATH} && \
	python -m pip install -U setuptools pip wheel twine urllib3 && \
	ls ${VENV_DIR_PATH}

venv-install: ## Install Python packages
## Provide PACKAGE_NAME=<package_name> to install a specific package
## Example: make venv-install PACKAGE_NAME=requests
	@if [[ -f "${REQUIREMENTS_FILE_PATH}" ]]; then \
		echo "Installing packages from ${REQUIREMENTS_FILE_PATH}" && \
		ls ${REQUIREMENTS_FILE_PATH} && \
		pip install -r "${REQUIREMENTS_FILE_PATH}" ${PACKAGE_NAME} ; \
	elif [[ -n "${PACKAGE_NAME}" ]]; then \
		echo "Installing package ${PACKAGE_NAME}" ; \
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

venv-run: ## Run main app script
	@python main.py

venv-test: ## Run tests
	python -m unittest discover -s tests -p 'test_*.py'

venv-test-clean:
	rm -f ${ROOT_DIR}/tests/data/input/*.output.*

.venv-build: 
	python setup.py sdist bdist_wheel

.venv-publish: 
	twine upload dist/*

.venv-validate-release-package:
	twine check ${ROOT_DIR}/dist/*	
# --- VENV --- END --------------------------------------------------------------


# --- Release --- START ------------------------------------------------------------
##
###Release
##---
validate-release-version: validate-PACKAGE_VERSION 
	@echo ${PACKAGE_VERSION} > ${ROOT_DIR}/version && \
	${ROOT_DIR}/scripts/version_validation.sh ${PACKAGE_VERSION}

build: .venv-build ## Build the package

validate-release-package: .venv-validate-release-package ## Validate the package with twine

publish: .venv-publish ## Publish the package
# --- Release --- END --------------------------------------------------------------



# --- Wrapper --- START ------------------------------------------------------------
##
###Wrapper
##---
wrapper-prepare-test:
	$(MAKE) audacity-kill || true
	$(MAKE) venv-test-clean
	$(MAKE) audacity-start
# --- Wrapper --- END --------------------------------------------------------------
