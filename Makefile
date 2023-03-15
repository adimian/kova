.PHONY: develop


develop:
	pip install poetry
	poetry install
	pre-commit install
