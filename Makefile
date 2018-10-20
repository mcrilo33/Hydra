.PHONY: help init update test

.DEFAULT: help
help:
	@echo "make init"
	@echo "		initialized environment, use only once"
	@echo "make update"
	@echo "		update everything"
	@echo "make test"
	@echo "		run tests"

init:
	pip install -r requirements.txt
	git submodule init && git submodule update

update: requirement
	git pull && git submodule update
requirement: requirements.txt
	pip install -r requirements.txt

test:
	python main.py --test
