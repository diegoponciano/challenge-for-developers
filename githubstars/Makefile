install:
	pip install -r requirements.txt

runserver:
	python manage.py runserver

test:
	DATABASE_URL="sqlite://:memory:" pytest -svlx

tests: test

coverage: clean
	DATABASE_URL="sqlite://:memory:" pytest --cov --cov-report html:coverage --cov-report xml --cov-report term-missing

lint:
	flake8

clean:
	rm -rf .coverage coverage coverage.xml .cache

