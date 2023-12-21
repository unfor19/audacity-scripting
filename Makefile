#!make
.ONESHELL:
.EXPORT_ALL_VARIABLES:
.PHONY: all $(MAKECMDGOALS)


UNAME := $(shell uname)
ROOT_DIR:=${CURDIR}
BASH_PATH:=$(shell which bash)

AUDACITY_VERSION:=3.4.2


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
AUDACITY_DOWNLOAD_PATH:=${ROOT_DIR}/audacity-installer.exe
AUDACITY_CHECKSUM:=D7BD5AE775DB9E42DA6058DA4A65A8F898A46CE467D9F21585084566213C36BF
AUDACITY_DOWNLOAD_URL:=https://github.com/audacity/audacity/releases/download/Audacity-${AUDACITY_VERSION}/audacity-win-${AUDACITY_VERSION}-64bit.exe
PIPELIST_DOWNLOAD_PATH:=${ROOT_DIR}/pipelist.zip
PIPELIST_CHECKSUM:=7BFEF3046BFCCE3EFA666C4AE235B3A903DDC8DDBA830A5C3EE4178E0A712B8D
PIPELIST_DOWNLOAD_URL:=https://download.sysinternals.com/files/PipeList.zip
PIPELIST_EXTRACTED_DIR_PATH:=${ROOT_DIR}/.pipelist
PIPELIST_EXTRACTED_FILE_PATH:=${PIPELIST_EXTRACTED_DIR_PATH}/pipelist64.exe

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

print-vars: ## Print env vars
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
pipelist-verify-checksum: validate-PIPELIST_DOWNLOAD_PATH validate-PIPELIST_CHECKSUM ## Verify pipelist checksum
	@echo "Verifying checksum for ${PIPELIST_DOWNLOAD_PATH} ..."
	@echo "Expected checksum: ${PIPELIST_CHECKSUM}"
	@python ${ROOT_DIR}/scripts/verify_checksum.py ${PIPELIST_DOWNLOAD_PATH} ${PIPELIST_CHECKSUM} sha256

.pipelist-download: validate-PIPELIST_DOWNLOAD_PATH validate-PIPELIST_DOWNLOAD_URL # A helper function to download pipelist
	@echo "Downloading pipelist ..."
	@curl -s -L ${PIPELIST_DOWNLOAD_URL} -o ${PIPELIST_DOWNLOAD_PATH}

pipelist-download: .pipelist-download pipelist-verify-checksum ## Download pipelist

pipelist-install: validate-PIPELIST_DOWNLOAD_PATH ## Install pipelist
	@echo "Installing pipelist ..."
	unzip -o ${PIPELIST_DOWNLOAD_PATH} -d ${PIPELIST_EXTRACTED_DIR_PATH} && \
		cp ${PIPELIST_EXTRACTED_FILE_PATH} c:/Windows/System32/pipelist.exe && \
		cp ${PIPELIST_EXTRACTED_FILE_PATH} c:/Windows/System32/pipelist64.exe

audacity-verify-checksum: validate-AUDACITY_DOWNLOAD_PATH validate-AUDACITY_CHECKSUM ## Verify Audacity checksum
	@echo "Verifying checksum for ${AUDACITY_DOWNLOAD_PATH} ..."
	@echo "Expected checksum: ${AUDACITY_CHECKSUM}"
	@python ${ROOT_DIR}/scripts/verify_checksum.py ${AUDACITY_DOWNLOAD_PATH} ${AUDACITY_CHECKSUM} sha256

.audacity-download: validate-AUDACITY_DOWNLOAD_URL validate-AUDACITY_DOWNLOAD_PATH # A helper function to download Audacity
	@echo "Downloading Audacity ..."
	@curl -s -L ${AUDACITY_DOWNLOAD_URL} -o ${AUDACITY_DOWNLOAD_PATH}

audacity-download: .audacity-download audacity-verify-checksum ## Download Audacity

audacity-install: validate-AUDACITY_DOWNLOAD_PATH ## Install Audacity
	@echo "Installing Audacity ..."
	powershell -c "${AUDACITY_DOWNLOAD_PATH} /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /NOICONS /NOCANCEL /SP- /LOG=${ROOT_DIR}/audacity-installer.log"
	@echo "Waiting for Audacity to complete installation ..."
	@until ls ${AUDACITY_BIN_PATH} ; do echo "Sleeping ..." && sleep 1 ; done
	@if [[  "${CI}" = "true" ]]; then \
		echo "Sleeping 10 seconds to allow Audacity to finish the installation ..." ; \
		sleep 10 ; \
		echo "Hopefully Audacity is up" ; \
	fi

audacity-update-config: validate-AUDACITY_PREFERENCES_PATH ## Update Audacity config
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

audacity-print-config: validate-AUDACITY_PREFERENCES_PATH ## Print Audacity config
	@if [[ -f "${AUDACITY_PREFERENCES_PATH}" ]]; then \
		cat "${AUDACITY_PREFERENCES_PATH}" ; \
	else \
		echo "ERROR: ${AUDACITY_PREFERENCES_PATH} file not found" ; \
		exit 1 ; \
	fi

audacity-start: validate-AUDACITY_BIN_PATH ## Start Audacity GUI app
	@echo Starting Audacity ...
	@${AUDACITY_BIN_PATH} &
	@if [[ "${_CI}" = "true" ]]; then \
		echo "Sleeping 10 seconds to allow Audacity to start the pipes ..." ; \
		sleep 10 ; \
		echo "Hopefully Audacity is up" ; \
	fi

audacity-test-pipe: ## Test Audacity pipe
	python ${ROOT_DIR}/scripts/audacity_pipetest.py

audacity-kill: validate-AUDACITY_KILL_COMMAND ## Kill Audacity
	${AUDACITY_KILL_COMMAND}

audacity-restart: audacity-kill audacity-start

# --- Audacity --- END --------------------------------------------------------------


# --- VENV --- START ------------------------------------------------------------
## 
##VENV
##----
venv-prepare: ## Create a Python virtual environment with venv
	python -m venv ${VENV_DIR_PATH} && \
	python -m pip install -U pip wheel && \
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
		pip install -U ${PACKAGE_NAME} ; \
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

venv-test-unittests: ## Run unit tests
	python -m unittest discover -s tests -p 'test_*.py'

venv-test: venv-test-unittests

venv-test-cli: venv-install-edit ## Run CLI tests
	audacity_scripting clean-spaces --file_path ${ROOT_DIR}/tests/data/input/1.aup3

venv-test-clean:
	rm -f ${ROOT_DIR}/tests/data/input/*.output.*

.venv-build: 
	python -m build .

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

wrapper-run-test: wrapper-prepare-test
	sleep 6
	$(MAKE) venv-test
# --- Wrapper --- END --------------------------------------------------------------
