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

# TODO: Set it - currently getting it from GitHub Actions on Windows
ifeq ($${CI},true)
AUDACITY_PREFERENCES_PATH:=/C/Users/runneradmin/AppData/Roaming/audacity/audacity.cfg
else
AUDACITY_PREFERENCES_PATH:=$${AUDACITY_PREFERENCES_PATH}
endif


# --- OS Settings --- START ------------------------------------------------------------
# Windows
ifneq (,$(findstring NT, $(UNAME)))
_OS:=windows
VENV_BIN_ACTIVATE:=${VENV_DIR_PATH}/Scripts/activate.bat
AUDACITY_BIN_PATH:="C:\Program Files\Audacity\audacity.exe"
AUDACITY_TARGET_CONFIG_PATH:="C:\Program Files\Audacity\audacity.cfg"
AUDACITY_KILL_COMMAND:=powershell -c "taskkill /F /IM Audacity.exe /T"
endif
# macOS
ifneq (,$(findstring Darwin, $(UNAME)))
_OS:=macos
AUDACITY_BIN_PATH:=/Applications/Audacity.app/Contents/MacOS/Wrapper
AUDACITY_TARGET_CONFIG_PATH:=/Applications/Audacity.app/Contents/audacity.cfg
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
	echo "AUDACITY_SRC_CONFIG_PATH=${AUDACITY_SRC_CONFIG_PATH}"
	echo "AUDACITY_BIN_PATH=${AUDACITY_BIN_PATH}"
	echo "AUDACITY_TARGET_CONFIG_PATH=${AUDACITY_TARGET_CONFIG_PATH}"
	echo "VENV_BIN_ACTIVATE=${VENV_BIN_ACTIVATE}"
	echo "REQUIREMENTS_FILE_PATH=${REQUIREMENTS_FILE_PATH}"
	echo "VENV_DIR_PATH=${VENV_DIR_PATH}"

# --- Audacity --- START ------------------------------------------------------------
##
##AUDACITY
##--------
audacity-copy-config:
	@echo Copying ${AUDACITY_SRC_CONFIG_PATH} file to ${AUDACITY_TARGET_CONFIG_PATH}
	@cp ${AUDACITY_SRC_CONFIG_PATH} ${AUDACITY_TARGET_CONFIG_PATH}

audacity-update-config:
	if [[ -f "${AUDACITY_PREFERENCES_PATH}" ]]; then \
		echo "Updating ${AUDACITY_PREFERENCES_PATH} file" ; \
		sed -i.bak 's/mod-script-pipe=4/mod-script-pipe=1/g' "${AUDACITY_PREFERENCES_PATH}" ; \
	fi

audacity-start: ## Start Audacity GUI app
	@echo Starting Audacity
	@${AUDACITY_BIN_PATH} &

audacity-kill:
	${AUDACITY_KILL_COMMAND}

audacity-print-custom-config:
	@if [[ -f ${AUDACITY_TARGET_CONFIG_PATH} ]]; then \
		cat ${AUDACITY_TARGET_CONFIG_PATH} ; \
	else \
		echo "ERROR: ${AUDACITY_TARGET_CONFIG_PATH} file not found" ; \
		exit 1 ; \
	fi
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

venv-run: audacity-start ## Run main app script
	@python main.py

venv-test: audacity-start ## Run tests
	python -m unittest discover -s tests -p 'test_*.py'

venv-test-clean:
	rm -f ${ROOT_DIR}/tests/data/*.trimmed.*
# --- VENV --- END --------------------------------------------------------------
