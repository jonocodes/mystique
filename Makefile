
test:
	pytest

setup:
	pip install -r requirements.txt -r requirements_dev.txt

build:
	python -m build

clean:
	rm -f dist/*

dist: clean build
	python -m twine upload --verbose -u=__token__ dist/*
