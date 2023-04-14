# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Bao Project and Contributors. All rights reserved

root_dir:=$(realpath .)
ci_dir:=$(root_dir)

all:

include ci.mk

python_scripts:= \
	$(root_dir)/misra/deviation_suppression.py \
	$(root_dir)/license_check.py \
	$(root_dir)/spell_check.py   \
	$(root_dir)/rops_check.py
$(call ci, pylint, $(python_scripts))

yaml_files:= \
	$(root_dir)/misra/deviation_record_template.yml \
	$(root_dir)/misra/deviation_permit_template.yml
$(call ci, yamllint, $(yaml_files))

c_files:=$(root_dir)/cppcheck-types.c
mk_files:=$(root_dir)/Makefile $(root_dir)/ci.mk

all_files:=$(python_scripts) $(yaml_files) $(c_files) $(mk_files)

$(call ci, license, "Apache-2.0", $(all_files))

ci: license-check pylint yamllint
