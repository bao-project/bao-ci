# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Bao Project and Contributors. All rights reserved

ROOT_DIR?=$(realpath ../..)

DOCKER?=$(shell which docker)
docker_repo:=baoproject/bao
docker_tag:=latest
docker_image:=$(docker_repo):$(docker_tag)
DOCKER_PULL?=y
ifeq ($(DOCKER_PULL),y)
docker_pull_option:=--pull=always
endif
docker_run_cmd:=$(DOCKER) run $(docker_pull_option) --rm -it -u bao -v \
	$(ROOT_DIR):$(ROOT_DIR) -w $(ROOT_DIR) $(docker_image)

override MAKEFLAGS:=$(addprefix -,$(MAKEFLAGS)) --no-print-directory

all .DEFAULT:
	@echo "Launching docker container..."
	@$(docker_run_cmd) $(MAKE) $(MAKEFLAGS) $(MAKEOVERRIDES) $@
	@echo "Leaving and destroying docker container..."

shell:
	@$(docker_run_cmd)

build:
	@echo "Launching docker container..."
	@$(DOCKER) build -t $(docker_image) .

push: build
	@echo "Pushing container image to $(docker_repo)"
	@$(DOCKER) push $(docker_image)

.PHONY: all build push shell
