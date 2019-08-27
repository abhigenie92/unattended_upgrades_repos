SHELL := /bin/bash

all: format test

format:
	black . 
test:
	nosetests -v .

.PHONY: format test all

