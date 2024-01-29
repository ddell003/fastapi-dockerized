.DEFAULT_GOAL := up

up:
	docker compose up -d

logs:
	docker logs -f api_dev

down:
	docker compose down

rebuild:
	docker compose up -d --build

shell:
	docker exec -it api_dev sh

dev.setup:
	./scripts/dev-setup.sh

dev.format:
	black api tests alembicsetup

dev.test:
	pytest -v --cov api --cov-report term-missing

dev.lint:
	flake8 api --show-source --statistics

docs:
	./scripts/generate-docs.sh

docs.html:
	./scripts/generate-html.sh

# -------------------------
# Alembic
# -------------------------
db.create:
	docker exec -it db psql -U postgres -c "CREATE DATABASE sfa_db;"

db.seed:
	docker exec -it api_dev sh -c "python3 -m api.helpers.load_data"

db.upgrade:
	docker run --rm \
		--network api-network \
		-v ${PWD}/alembic:/opt/alembic \
		-v ${PWD}/api:/opt/api \
		-e DB_HOST=db \
    -e DB_PORT=5432 \
    -e DB_NAME=sfa_db \
    -e DB_USERNAME=postgres \
    -e DB_PASSWORD=postgres \
		dockerized-fastapi-api  \
		alembic upgrade head

db.downgrade:
	docker run --rm \
		--network api-network \
		-v ${PWD}/alembic:/opt/alembic \
		-v ${PWD}/api:/opt/api \
		-e DB_HOST=db \
    -e DB_PORT=5432 \
    -e DB_NAME=sfa_db \
    -e DB_USERNAME=postgres \
    -e DB_PASSWORD=postgres \
		dockerized-fastapi-api  \
		alembic downgrade base

db.current:
	docker run --rm \
		--network api-network \
		-v ${PWD}/alembic:/opt/alembic \
		-e DB_HOST=db \
    -e DB_PORT=5432 \
    -e DB_NAME=postgres \
    -e DB_USERNAME=postgres \
    -e DB_PASSWORD=postgres \
		dockerized-fastapi-api  \
		alembic current

db.upgrade.test:
	docker run --rm \
		--network api-network \
		-v ${PWD}/alembic:/opt/alembic \
		-v ${PWD}/test_data:/opt/data \
		-v ${PWD}/api:/opt/api \
		-e DB_HOST=db \
    -e DB_PORT=5432 \
    -e DB_NAME=postgres \
    -e DB_USERNAME=postgres \
    -e DB_PASSWORD=postgres \
		dockerized-fastapi-api  \
		alembic upgrade head
