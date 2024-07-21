setup:
	pip install -r requirements.txt -r requirements_dev.txt

build: setup
	python -m build

clean:
	rm -f dist/*

test:
	pytest

dist: clean build
	python -m twine upload --verbose -u=__token__ dist/*
