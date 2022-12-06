.PHONY: clean lint download install docker push format tensorboard data train

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = room-graph
SRC_DIR = roomgraph

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Set up python interpreter environment
create_environment:
	@echo ">>> Creating environment"
	poetry config virtualenvs.create true
	poetry config virtualenvs.in-project true

## Install Python Dependencies
install: create_environment
	@echo ">>> Installing python dependencies"
	poetry update --lock # ensures all dependencies are as up-to-date as possible
	poetry install

## Make Dataset
download:
	mkdir data/raw
	wget "https://zenodo.org/record/2613548/files/cubicasa5k.zip?download=1"
	unzip cubicasa5k.zip -d data/raw
	rm -rf cubicasa5k.zip

data: download
	@echo ">>> Making dataset"
	poetry run make_dataset

## Training (Example Version)
train: data
	@echo ">>> Training"
	poetry run train models/example

tensorboard:
	@echo ">>> Running tensorboard"
	poetry run tensorboard --logdir=models

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
lint:
	flake8 $(SRC_DIR)

## Format using black
format:
	black $(SRC_DIR)

## Run bandit security test
bandit:
	poetry run bandit -n 3 -r $(SRC_DIR)

test:
	poetry run pytest

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
