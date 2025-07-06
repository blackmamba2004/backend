Запустить проект локально в первый раз(для linux)

1. Собрать контейнеры
docker compose --profile local-environment up --build

2. Поднять контейнеры с БД и Redis
docker compose -f docker-compose.dev.yaml --profile local-environment up -d

3. Создать суперюзера
cat cmd/admin/create-super-user.sql | docker exec -i cars-api-db psql -U postgres -d app

4. Запустить основное приложение FastAPI на uvicorn
bash cmd/start/local.sh

5. Остановить контейнеры с БД и Redis
docker compose -f docker-compose.dev.yaml --profile local-environment down


Запустить проект в режиме разработки(dev)

1. Собрать контейнеры
docker compose -f docker-compose.dev.yaml --profile dev-backend-container build

2. Поднять контейнеры
docker compose -f docker-compose.dev.yaml --profile dev-backend-container up

3. Остановить контейнеры
docker compose -f docker-compose.dev.yaml --profile dev-backend-container down


Вспомогательные команды

rm -rf ./data - для удаления данных из БД и Redis

cat cmd/admin/create-super-user.sql | docker exec -i cars-api-db psql -U postgres -d app - создать суперюзера