.PHONY: install-main install-main-and-dev lint format-code run

install-main:
	poetry shell;
	poetry install --only main

install-main-and-dev:
	poetry shell;
	poetry install

lint:
	poetry run mypy .

format-code:
	poetry run autoflake .; 
	poetry run isort .; 
	poetry run black .

run:
	poetry run python3 metro_parser/main.py
