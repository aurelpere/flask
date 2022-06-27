install:
	pip3 install --upgrade pip &&\
		pip3 install -r requirements.txt
format:
	yapf -ir -vv --style pep8 .
lint:
	cd ..; pylint app --verbose --disable=R,C -sy
test:
	pytest -vv . --cov=. --cov-report xml:reports/coverage/coverage.xml
docker:
	docker-compose build && docker-compose up -d
all: install format lint test docker