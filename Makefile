.PHONY: test run clean

test:
	python3 -m unittest discover tests

run:
	python3 -m plllu.run_plllu

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete