linux-build-dev:
	docker compose --profile local-environment up --build

linux-up-dev:
	docker compose --profile local-environment up
#	python3.12 app/main-dev.py
