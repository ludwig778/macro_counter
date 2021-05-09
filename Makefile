default: prompt

prompt:
	python3 -m macro_counter

py:
	python3

sh:
	bash

lint:
	python3 -m flake8 .

isort:
	python3 -m isort .

piprot:
	piprot

sure: lint isort piprot

clean:
	rm -rf coverage_html
	find . -name "*.pyc" -o -name "__pycache__"|xargs rm -rf
