#!/bin/bash
SHELL := /bin/bash


.PHONY: all test clean full_clean

MKFILE_PATH := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

PY?=python
DEPS?=$(MKFILE_PATH)deps/local.txt

APPS=$(MKFILE_PATH)apps
ENV=$(MKFILE_PATH)menv
BUILD=$(MKFILE_PATH)build

ACTIVATE=`source $(ENV)/Scripts/activate`
SETUP_ENV=`virtualenv --python=$(PY) $(ENV)`


all: runservt


runservt: make_and_migrate test runserv

rs: runserv # Alias for runserv

runserv: make_and_migrate
	(\
	$(ACTIVATE) && \
	$(PY) $(APPS)/manage.py runserver
	)


test: make_and_migrate
	(\
	$(ACTIVATE) && \
	$(PY) $(APPS)/manage.py test $(APPS)
	)

make_and_migrate: make_migrs migrate

migrate: install_deps
	(\
	$(ACTIVATE) && \
	$(PY) $(APPS)/manage.py migrate
	)

make_migrs: install_deps
	(\
	$(ACTIVATE) && \
	$(PY) $(APPS)/manage.py makemigrations
	)


install_deps: create_env
	(\
	$(ACTIVATE)
	pip install -r $(DEPS); \
	)

create_env: mkbdir
	# Create venv if `$(BUILD)/env_lock` is not created
	virtualenv --python=$(PY) $(ENV)
	#@test -s $(BUILD)/env_lock || { $(SETUP_ENV); echo 'venv created' >$(BUILD)/env_lock; }

mkbdir:
	@cd $(MKFILE_PATH) && mkdir -p build


full_clean: clean
	cd $(APPS) && \
	rm -rf db.sqlite3 && \
	find . -name \*.pyc -delete

clean:
	cd $(MKFILE_PATH) && rm -rf build
