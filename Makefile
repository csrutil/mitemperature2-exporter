NAME=mitemperature2-exporter

.PHONY : install run

run:
	@poetry run python mitemperature2_exporter/app.py

install:
	@poetry install --only main

lint:
	@poetry run black mitemperature2_exporter
	@poetry run flake8 mitemperature2_exporter --count --statistics

test:
	@echo Not Implemented
