.PHONY: help build build-frontend build-backend up up-build down down-clean restart logs logs-frontend logs-backend shell web-shell db-shell test migrate makemigrations collectstatic createsuperuser clean destroy

# Default environment
ENV ?= development

install-docker-compose:
	apt install docker-compose

help:
	@echo "Django + React + PostgreSQL Docker Makefile"
	@echo ""
	@echo "Available commands:"
	@echo "  build           Build or rebuild all services"
	@echo "  build-frontend  Build only the frontend service"
	@echo "  build-backend   Build only the backend service"
	@echo "  up              Create and start all containers"
	@echo "  up-frontend     Start only the frontend service"
	@echo "  up-backend      Start only the backend service"
	@echo "  down            Stop and remove containers"
	@echo "  down-clean      Stop and remove containers, networks, and volumes"
	@echo "  restart         Restart all services"
	@echo "  logs            View output from all containers"
	@echo "  logs-frontend   View frontend logs"
	@echo "  logs-backend    View backend logs"
	@echo "  shell           Access backend container shell"
	@echo "  frontend-shell  Access frontend container shell"
	@echo "  db-shell        Access database container shell"
	@echo "  test            Run Django tests"
	@echo "  migrate         Run Django migrations"
	@echo "  makemigrations  Create new Django migrations"
	@echo "  collectstatic   Collect Django static files"
	@echo "  createsuperuser Create Django superuser"
	@echo "  clean           Remove all containers, images, and volumes"

# Build all services
build:
	docker-compose build

# Build only frontend
build-frontend:
	docker-compose build react-frontend

# Build only backend
build-backend:
	docker-compose build django-web

# Start all services in detached mode
up:
	docker-compose up -d

# Start services with build
up-build:
	docker-compose up -d --build

# Start only frontend
up-frontend:
	docker-compose up -d react-frontend

# Start only backend
up-backend:
	docker-compose up -d django-web db

# Stop and remove containers
down:
	docker-compose down

# Stop and remove containers, networks, and volumes
down-clean:
	docker-compose down -v --remove-orphans

# Restart services
restart:
	docker-compose restart

# View all logs
logs:
	docker-compose logs -f

# View frontend logs
logs-frontend:
	docker-compose logs -f react-frontend

# View backend logs
logs-backend:
	docker-compose logs -f django-web

# Access backend container shell
shell:
	docker-compose exec django-web /bin/bash

# Access frontend container shell
frontend-shell:
	docker-compose exec react-frontend /bin/sh

# Access database container shell
db-shell:
	docker-compose exec db psql -U ${DATABASE_USERNAME} -d ${DATABASE_NAME}

# Run Django tests
test:
	docker-compose exec django-web python manage.py test

# Run Django migrations
migrate:
	docker-compose exec django-web python manage.py migrate

# Create new Django migrations
makemigrations:
	docker-compose exec django-web python manage.py makemigrations

# Collect Django static files
collectstatic:
	docker-compose exec django-web python manage.py collectstatic --noinput

# Create Django superuser
createsuperuser:
	docker-compose exec django-web python manage.py createsuperuser

# Clean everything (containers, images, volumes)
clean:
	docker-compose down -v --remove-orphans
	docker system prune -a -f

# Destroy everything including volumes
destroy:
	docker-compose down -v --remove-orphans --rmi all

# Production build for frontend (creates optimized build)
build-frontend-prod:
	docker-compose run --rm react-frontend npm run build

# Install new frontend dependencies
frontend-install:
	docker-compose run --rm react-frontend npm install

# Install new backend dependencies
backend-install:
	docker-compose run --rm django-web pip install -r requirements.txt