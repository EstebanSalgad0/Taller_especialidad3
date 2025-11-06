SHELL := /bin/sh

.PHONY: up down ps logs build scale backup restore image-size

up:
	docker compose up -d

down:
	docker compose down --volumes --remove-orphans

ps:
	docker compose ps

logs:
	docker compose logs -f

build:
	docker compose build

scale:
	docker compose up -d --scale api=2

# Create a SQL dump from the running db container to backup.sql
backup:
	docker compose exec -T db pg_dump -U $${DB_USER} -d $${DB_NAME} > backup.sql

# Restore backup.sql into the running db (DB must exist)
restore:
	docker compose exec -T db psql -U $${DB_USER} -d $${DB_NAME} < backup.sql

image-size:
	docker image ls --format "{{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep catalogo_api || true
DB_PASSWORD := my_db_password