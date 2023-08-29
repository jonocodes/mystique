
test:
	pytest

build:
	python3 -m build

clean:
	rm -f dist/*

dist: clean build
	python3 -m twine upload --verbose -u=__token__ dist/*
