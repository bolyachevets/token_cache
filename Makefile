MKFILE_PATH:=$(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_ABS_DIR:=$(patsubst %/,%,$(dir $(MKFILE_PATH)))

PROJECT_NAME:=auth_api
DOCKER_NAME:=auth-api

#################################################################################
# COMMANDS -- Setup                                                             #
#################################################################################
setup: clean install install-dev ## Setup the project

clean: clean-build clean-pyc
	rm -rf venv/

clean-build: ## Clean build files
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

clean-pyc: ## Clean cache files
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

install: clean ## Install python virtrual environment
	test -f venv/bin/activate || python3.10 -m venv  $(CURRENT_ABS_DIR)/venv ;\
	. venv/bin/activate ;\
	pip install --upgrade pip ;\
	pip install -Ur requirements.txt

install-dev: ## Install local application
	. venv/bin/activate ; \
	pip install -Ur requirements/dev.txt; \
	pip install -e .

#################################################################################
# COMMANDS - Local                                                              #
#################################################################################
run: ## Run the project in local
	. venv/bin/activate && python3.10 -m flask run -p 5000
