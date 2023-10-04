
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

.PHONY: all build push deploy docker-login

all: build

build: Dockerfile *.py
	 docker compose build

push: build docker-login
	docker compose push

docker-login:
	@echo "Logging in to ghcr.io"
	@echo ${CR_PAT} | docker login ghcr.io -u USERNAME --password-stdin
