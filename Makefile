# make build name=pk3proc

build:
	@echo build: $(name)
	@rm -rf dist
	MOD=$(name) python make-setup.py
	python setup.py sdist
	twine upload dist/*
