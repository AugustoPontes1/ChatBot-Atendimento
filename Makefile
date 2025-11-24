.PHONY: help build up down restart logs shell web-shell db-shell test migrate makemigrations collectstatic createsuperuser clean destroy

# Default environment
ENV ?= development

install-docker-compose:
	apt install docker-compose

help:
	@echo "Django + PostgreSQL Docker Makefile"
	@echo ""
	@echo "Available commands:"
	@echo "  build           Build or rebuild services"
	@echo "  up              Create and start containers"
	@echo "  down            Stop and remove containers"
	@echo "  restart         Restart all services"
	@echo "  logs            View output from containers"

# Build the services
build:
	docker-compose build

# Start services in detached mode
up:
	docker-compose up -d

# Start services with build
up-build:
	docker-compose up -d --build

# Stop and remove containers
down:
	docker-compose down

# Restart services
restart:
	docker-compose restart

# View logs
logs:
	docker-compose logs -f
