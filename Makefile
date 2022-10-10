.DEFAULT_GOAL :=help
.PHONY: venv
.EXPORT_ALL_VARIABLES:

## GENERAL ##
PROJECT_NAME	= services
IMAGE_BACKEND	= $(PROJECT_NAME)-backend:dev
CONTAINER_BACKEND	= $(PROJECT_NAME)_backend
DOCKER_NETWORK = zebrand_network


build: ## construir imagenes: make build
	@docker-compose -p $(PROJECT_NAME) build

up: ## levantar servicios: make up
	@make network &> /dev/null
	@docker-compose -p $(PROJECT_NAME) up -d
	@docker-compose -p $(PROJECT_NAME) ps

down: ## apagar servicios: make down
	@docker-compose -p $(PROJECT_NAME) down

clean-cache: ## remover archivos __pycache__: make clean-cache
	@sudo sh -c 'find . | grep -E "(__pycache__|\.pyc|\.pyo$|.pytest_cache)" | xargs rm -rf'

log: ## mostrar logs: make log
	@docker logs -f $(CONTAINER_BACKEND)

status: ## mostrar estado: make status
	@docker-compose -p $(PROJECT_NAME) ps

ssh: ## acceder contenedor: make ssh
	@docker exec -it $(CONTAINER_BACKEND) bash

## MIGRATION TARGETS ##
revision: ## crear migración: make revision DESC="brief description"
	@docker run --rm --tty --volume $(PWD):/app:rw --network $(DOCKER_NETWORK) \
		--entrypoint="/alembic" $(IMAGE_BACKEND) revision -m "$(DESC)"
	@sudo chown -R $(USER):$(USER) $(PWD)/alembic/versions

migrate: ## ejecuta migrate: make migrate
	@docker run --rm --tty --volume $(PWD):/app:rw --network $(DOCKER_NETWORK) \
		--entrypoint="/alembic" $(IMAGE_BACKEND) upgrade head

rollback: ## ejecuta rollback: make rollback
	@docker run --rm -t -v $(PWD):/app:rw --network $(DOCKER_NETWORK) \
		--entrypoint="/alembic" $(IMAGE_BACKEND) downgrade -1

network: ## verifica si existe la red, caso contrario la crea: make network
	@if [ -z $$(docker network ls | grep $(DOCKER_NETWORK) | awk '{print $$2}') ]; then\
		(docker network create $(DOCKER_NETWORK));\
	fi

## HELP TARGET ##
help:
	@printf "\033[31m%-22s %-59s %s\033[0m\n" "Target" " Help" "Usage"; \
	printf "\033[31m%-22s %-59s %s\033[0m\n"  "------" " ----" "-----"; \
	grep -hE '^\S+:.*## .*$$' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' | sort | awk 'BEGIN {FS = ":"}; {printf "\033[32m%-22s\033[0m %-58s \033[34m%s\033[0m\n", $$1, $$2, $$3}'
