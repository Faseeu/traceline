.PHONY: install test lint format up down

install:
	uv sync

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff format .
	uv run ruff check --fix .

up:
	docker compose up -d

down:
	docker compose down
