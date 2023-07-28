# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Bao Project and Contributors. All rights reserved

root_dir?=$(realpath ..)
nix_dir:=$(realpath .)

#############################################################################
override MAKEFLAGS:=$(addprefix -,$(MAKEFLAGS)) --no-print-directory

all .DEFAULT:
	@echo "Launching nix-shell..."
	@nix-shell $(nix_dir)/shell.nix --run \
		"$(MAKE) -C $(root_dir) $(MAKEFLAGS) $(MAKEOVERRIDES) $@"
	@echo "Leaving nix-shell..."

#############################################################################

# Nix-shell
# Provides a nix-shell with the bao-project environment (i.e, all bao-project
# dependencies) which can be used to run the commands/tools used accross all
# bao-project repositories.
# To open an interactive nix-shell with the bao-project environment:
#    make nix-shell
# To run a standalone command inside the nix-shell use:
#    make nix-shell-run cmd="command-to-run"
# @param The command to run inside the nix-shell.
# @example make nix-shell-run cmd="ls"

nix-shell:
	@nix-shell $(nix_dir)/shell.nix

nix-shell-run:
	@nix-shell $(nix_dir)/shell.nix --run "$(cmd)"

.PHONY: all
non_build_targets+=nix-shell nix-shell-run

define nix-shell-run
cmd:=$1
endef