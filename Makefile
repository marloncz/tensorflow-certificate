#################################################################################
# GLOBALS                                                                       #
#################################################################################

ENVNAME := .venv
VENV := $(ENVNAME)/bin

PROJECT_NAME = tensorflow-certificate
PYTHON_INTERPRETER = $(VENV)/python

#################################################################################
# SETUP
#################################################################################

.PHONY: install
install: install_tools install_dependencies install_kernel
	direnv allow

.PHONY: install_dependencies
install_dependencies: install_tools
	poetry config virtualenvs.in-project true
	poetry env use $$(pyenv prefix 3.8.0)/bin/python
	poetry install

.PHONY: install_tools
install_tools:
	@sh install_dependencies.sh

.PHONY: install_kernel
install_kernel:
	$(VENV)/python -m ipykernel install --user --name $(PROJECT_NAME)

