# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Bao Project and Contributors. All rights reserved

$(call check_variable_defined, root_dir, \
	"To include ci.mk the 'root_dir' must be defined")

ci_dir?=$(realpath $(root_dir)/ci)
cur_dir:=$(realpath .)

include $(ci_dir)/util.mk

CPPCHECK?=cppcheck
CLANG_VERSION?=14
CLANG-FORMAT?=clang-format-$(CLANG_VERSION)
CLANG-TIDY?=clang-tidy-$(CLANG_VERSION)

.SECONDEXPANSION:

#############################################################################

# Requirements for new targets:
# - Each non build target, should be added as a .PHONY target prerequiste.
# - The non_build_targets variable should be used to add targets that do not
#   perform a build step.

#############################################################################

# Git Commit message linting
# Checks if the commit messages follow the conventional commit style from 
# GITLINT_BASE to the last commit. For example, for checking the last two commits:
#    make gitlint GITLINT_BASE=HEAD~2

gitlint:
	@gitlint -C $(ci_dir)/.gitlint --commits $(GITLINT_BASE)..

.PHONY: gitlint
non_build_targets+=gitlint

#############################################################################

# License Checking
# Checks if the provided source file have a SPDX license identifier following
# the provided SPDX license expriession.
#    make license-check
# @param string of SPDX expression of the allowed license for the files defined
#    in the second param
# @param space-separated list of source files (any kind)
# @example $(call ci, license, "Apache-2.0 OR MIT", file1.c file.rs file.h file.mk)

license_check_script:=$(ci_dir)/license_check.py

license-check:
	@$(license_check_script) -l $(spdx_expression) $(license_check_files)

.PHONY: license-check
non_build_targets+=license-check

define license
spdx_expression:=$1
license_check_files:=$2
endef

#############################################################################

# Python linting
# Checks if the provided python scrpits for syntax and format:
#    make pylint
# @param space-separated list of python files
# @example $(call ci, pylint, file1.py file2.py)

pylintrc:=$(ci_dir)/.pylintrc

pylint: $(pylintrc)
	@pylint $(_python_scritps)

.PHONY: pylint
non_build_targets+=pylint

define pylint
_python_scritps+=$1
endef

#############################################################################

# YAML linting
# Checks if the provided yaml files for syntax and format:
#    make yamllint
# @param space-separated list of yaml files
# @example $(call ci, yamllint, file1.yaml file2.yml)

yamllint:
	@yamllint --strict $(_yaml_files)

.PHONY: yamllint
non_build_targets+=yamllint

define yamllint
_yaml_files+=$1
endef

#############################################################################

# Spell checker
# Provides one make target:
#    make spell-check # check if the provided files are correctly spelled
#
# @param  -t {txt,yaml}, --type {txt,yaml}
#     The type of file to be spell-checked. Valid options are 'txt' and 'yaml'.
# @param   -k KEYS [KEYS ...], --keys KEYS [KEYS ...]
#     A space-separated list of keys to be excluded from spell-checking.
# @param   -f FILES [FILES ...], --files FILES [FILES ...]
#     A space-separated list of file paths to be spell-checked.
# @param   -d DICTIONARIES [DICTIONARIES ...], --dictionaries DICTIONARIES \
# [DICTIONARIES ...]
#     A space-separated list of additional dictionaries to be used for
#     spell-checking.
# @example $(call ci, spell_check, -t txt -f file1.txt file2.txt -d \
# custom_dict.txt)

.PHONY: spell-check
non_build_targets+=spell-check
spell-check:
	@$(ci_dir)/spell_check.py $(_spell_args)

define spell-check
_spell_args+=$1
endef

#############################################################################

# C Formatting
# Provides two make targets:
#    make format-check # checks if the provided C files are formated correctly
#    make format # formats the provided C files 
# @param space-separated list of C source or header files
# @example $(call ci, format, file1.c fil2.c file3.h)

format_file:=$(ci_dir)/.clang-format
clang_format_flags:=--style=file:$(format_file)

format:
	@$(CLANG-FORMAT) $(clang_format_flags) -i $(_format_files)

format-check:
	@diff <(cat $(_format_files)) <($(CLANG-FORMAT) $(clang_format_flags) $(_format_files))

.PHONY: format format-check
non_build_targets+=format format-check

define format
_format_files+=$1
endef

#############################################################################

# Clang-tidy linter
# To run the tidy linter:
#    make tidy
# @pre the make variable `clang-arch` must be defined if using the tidy rule
#    with a valid target fot the clang compiler
# @param files a single space-separated list of C files (header or source)
# @param paths a list of pre-processor options, specially the include
#    directory paths
# @example $(call ci, tidy, file1.c file2.c file3.h, -I/my/include/dir/inc)

tidy:
	@$(CLANG-TIDY) --config-file=$(ci_dir)/.clang-tidy $(_tidy_files) -- \
		--target=$(clang-arch) $(_tidy_flags) 2> /dev/null

.PHONY: tidy
non_build_targets+=tidy

define tidy
_tidy_files+=$1
_tidy_flags+=$2
endef

#############################################################################

# Cppcheck static-analyzer
# Run it by:
#    make cppcheck
# @pre the make variable 'cc' must be defined with the target's cross-compiler
#	to run any cppcheck-based rules
# @param files a single space-separated list of C files (header or source)
# @param headers a list of preprocessor flags, including header files root path
# @example $(call ci, cppcheck, file1.c file2.c file3.h, -I/my/include/dir/inc)

cppcheck_type_cfg:=$(ci_dir)/.cppcheck-types.cfg
cppcheck_type_cfg_src:=$(ci_dir)/cppcheck-types.c

$(cppcheck_type_cfg): $(cppcheck_type_cfg_src)
	@$(cc) -S -o - $< | grep "\->" | sed -r 's/.*->//g' > $@

cppcheck_suppressions:=$(ci_dir)/.cppcheck-suppress
cppcheck_flags:= --quiet --enable=all --error-exitcode=1 \
	--library=$(cppcheck_type_cfg) \
	--suppressions-list=$(cppcheck_suppressions) $(_cppcheck_flags)

cppcheck: $(cppcheck_type_cfg)
	@$(CPPCHECK) $(cppcheck_flags) $(_cppcheck_files)

cppcheck-clean:
	@rm -f $(cppcheck_type_cfg)

clean: cppcheck-clean

.PHONY: cppcheck
non_build_targets+=cppcheck cppcheck-clean

define cppcheck
$(call check_variable_defined, cc, \
	"For running cppcheck-based tests 'cc' must be defined")
_cppcheck_files+=$1
_cppcheck_flags+=$2
endef

#############################################################################

# MISRA Checker
# Use this rule to run the Cppcheck misra add-on checker:
#    make misra-check
# @pre MISRA checker rules assume your repository as a misra folder in the
#    top-level directories with the records and permits subdirectories (see doc).
# @param cfiles space separated list of C source files
# @param hfiles space separated list of C header files
# @param paths a list of preprocessor flags, including header files root path
# @param sups explicit space separated list of suppressions
# @example $(call ci, misra, file1.c file2.c, file3.h, -I/my/include/dir/inc,
# --suppress=<spec>)
# @note: check cppcheck help to know more about suppressions use

misra_ci_dir:=$(ci_dir)/misra
misra_rules:=$(misra_ci_dir)/rules.txt
misra_cppcheck_supressions:=$(misra_ci_dir)/.cppcheck-misra-unused-checks
misra_deviation_suppressions:=$(misra_ci_dir)/.cppcheck-misra-deviations
misra_deviation_suppressions_script:=$(misra_ci_dir)/deviation_suppression.py
misra_suppresions:=$(misra_ci_dir)/.cppcheck-misra-suppressions

misra_dir:=$(root_dir)/misra
misra_deviation_records:=$(misra_dir)/deviations/
misra_deviation_permits:=$(misra_dir)/permits/

define cppcheck_misra_addon
"{\
    \"script\": \"misra\",\
    \"args\": [\
        \"--rule-texts=$(root_dir)/ci/misra/rules.txt\"\
    ]\
}"
endef

cppcheck_misra_flags= --quiet --enable=all --error-exitcode=1 \
	--library=$(cppcheck_type_cfg) --addon=$(cppcheck_misra_addon) \
	--suppressions-list=$(misra_suppresions) $(_misra_flags)
zephyr_coding_guidelines:=https://raw.githubusercontent.com/zephyrproject-rtos/zephyr/main/doc/contribute/coding_guidelines/index.rst

ifeq ($(MISRA_C2012_GUIDELINES),)
$(misra_rules):
	@echo "Appendix A Summary of guidelines" > $@
	-@wget -q -O - $(zephyr_coding_guidelines) | \
		grep "\* -  Rule" -A 2 | sed -n '2~2!s/\(.\{9\}\)//p' >> $@
else
$(misra_rules):
	@pdftotext $(MISRA_C2012_GUIDELINES) $@
endif

$(misra_deviation_suppressions): $$(_misra_c_files) $$(_misra_h_files)
	@$(misra_deviation_suppressions_script) $^ > $@

$(misra_suppresions): $(misra_cppcheck_supressions) $(misra_deviation_suppressions)
	@cat $^ > $@

misra-check: $(misra_rules) $(cppcheck_type_cfg) $(misra_suppresions)
	@$(CPPCHECK) $(cppcheck_misra_flags) $(_misra_c_files) $(_misra_sup)

misra-clean:
	-rm -f $(misra_rules) $(misra_suppresions) $(misra_deviation_suppressions)

$(call ci, yamllint, $(wildcard $(misra_deviation_records) $(misra_deviation_permits)))

clean: misra-clean cppcheck-clean

.PHONY: misra-check misra-clean misra-dev-check
non_build_targets+=misra-check misra-clean

define misra
_misra_c_files+=$1
_misra_h_files+=$2
_misra_flags+=$3
_misra_sup+=$4
endef

#############################################################################

# Assembler Formatting
# Provides three make targets:
#    make asmfmt-check # checks if the provided assembly files are formated correctly
#    make asmfmt # formats the provided assembly files
# @param space-separated list of assembly files
# @example $(call ci, asmfmt, file1.S fil2.S file3.S)

asmfmt:
	@asmfmt -w $(_asm_files)

asmfmt-check:
	@diff <(cat $(_asm_files)) <(asmfmt $(_asm_files))

.PHONY: asmfmt asmfmt-check
non_build_targets+=asmfmt asmfmt-check

define asmfmt
_asm_files+=$1
endef

#############################################################################

# ROPs Checking
# Checks if the current working branch as increased or decreased the number of
# ROPs in final binary file. The call to this rule should take into account
# that any env variable that is used in the build command should be passed
# (e.g., PLATFORM=<platform>)
#    make rops-check ENVAR=<value>
# @param build command of the repo
# @param path to the binary file
# @example $(call ci, rops, make PLATFORM=qemu-aarch64-virt, bin/qemu-aarch64-virt/partitioner.elf)

rops_check_script:=$(ci_dir)/rops_check.py

rops-check:
	@$(rops_check_script) -b "$(build_cmd)" -x $(exe_path)

.PHONY: rops-check
non_build_targets+=rops-check

define rops
build_cmd:=$1
exe_path:=$2
endef

#############################################################################

ci=$(eval $(call $1, $2, $3, $4, $5, $6, $7, $8, $9))

