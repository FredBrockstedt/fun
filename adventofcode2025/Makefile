# Makefile for Advent of Code 2025

.PHONY: help venv

# Display this help message
help: 
	@# see: https://stackoverflow.com/questions/35730218/how-to-automatically-generate-a-makefile-help-command
	@echo "Usage: make <target>"
	@echo ""
	@echo "<target>     <description>"
	@echo "--------------------------"
	@awk '/^#/{c=substr($$0,3);next}c&&/^[[:alpha:]][[:alnum:]_-]+:/{print substr($$1,1,index($$1,":")),c}1{c=0}' $(MAKEFILE_LIST) | column -s: -t
	@echo ""

# Create a virtual environment for python
venv: .venv

.venv:
	@echo "* Creating virtual environment"
	uv venv 
	@echo "* Completed"
	@echo "  you can now load the virtual environment for this project"
	@echo "  with the commmand:"
	@echo "  $$ source .venv/bin/activate"


# Delete the virtual environment folder
clean-venv:
	rm -vr .venv || true
	rm -vr venv

# Install projects missing dependencies with, ideal run from a venv
dependencies:
	@echo "* Syncing with uv"
	@uv sync
