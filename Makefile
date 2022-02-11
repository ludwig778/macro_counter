ARGS = $(filter-out $@,$(MAKECMDGOALS))

TEST_ARGS = -vvss


default: prompt

prompt:
	poetry install
	macro_counter

sh:
	bash

py:
	ipython

lint:
	flake8

isort:
	isort macro_counter/ tests/

black:
	black .

mypy:
	mypy macro_counter

piprot:
	piprot pyproject.toml

debug:
	while :; do inotifywait -e modify -r .;make tests;sleep .2;done

tests:
	pytest ${TEST_ARGS}

test_on:
	pytest ${TEST_ARGS} ${ARGS}

cov:
	pytest ${TEST_ARGS} --cov=macro_counter

cov_html:
	pytest  ${TEST_ARGS} --cov=macro_counter --cov-report html:coverage_html

sure: tests lint mypy isort black piprot

publish:
	poetry build
	poetry publish

clean:
	rm -rf coverage_html .coverage .mypy_cache .pytest_cache
	find . -name "*.pyc" -o -name "__pycache__"|xargs rm -rf

.PHONY: tests
