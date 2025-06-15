local-build:
	docker compose --profile local-environment up --build

local-up:
	docker compose --profile local-environment up

build-dev:
	docker compose -f docker-compose.dev.yaml --profile dev-backend-container build

up-dev:
	docker compose -f docker-compose.dev.yaml --profile dev-backend-container up

down-dev:
	docker compose -f docker-compose.dev.yaml --profile dev-backend-container down