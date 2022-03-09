ci_dir?=$(realpath ci)

CPPCHECK?=cppcheck
CLANG_VERSION?=12
CLANG-FORMAT?=clang-format-$(CLANG_VERSION)
CLANG-TIDY?=clang-tidy-$(CLANG_VERSION)

.SECONDEXPANSION:

#############################################################################

pylintrc:=$(ci_dir)/.pylintrc

pylint: $(pylintrc)
	@pylint $(_python_scritps)

define pylint
_python_scritps+=$1
endef

#############################################################################

yamllint:
	@yamllint --strict $(_yaml_files)
.PHONY:yamllint

define yamllint
_yaml_files+=$1
endef

#############################################################################

clang_format_flags:=--style=file
format_file:=$(root_dir)/.clang-format
original_format_file:=$(ci_dir)/.clang-format

$(format_file): $(original_format_file)
	@cp $< $@

format: $(format_file)
	@$(CLANG-FORMAT) $(clang_format_flags) -i $(_format_files)

format-check: $(format_file)
	@diff <(cat $(_format_files)) <($(CLANG-FORMAT) $(clang_format_flags) $(_format_files))

format-clean:
	-@rm -f $(format_file)

clean: format-clean

.PHONY: format format-check format-clean
non_build_targets+=format format-check format-clean

define format
_format_files+=$1
endef

#############################################################################

tidy:
	@$(CLANG-TIDY) --config-file=$(ci_dir)/.clang-tidy $(_tidy_files) -- \
		--target=$(clang-arch) $(CPPFLAGS) 2> /dev/null

.PHONY: tidy
non_build_targets+=tidy

define tidy
_tidy_files+=$1
endef

#############################################################################

cppcheck_type_cfg:=$(ci_dir)/.cppcheck-types.cfg
cppcheck_type_cfg_src:=$(ci_dir)/cppcheck-types.c

$(cppcheck_type_cfg): $(cppcheck_type_cfg_src)
	@$(cc) -S -o - $< | grep "\->" | sed -r 's/.*->//g' > $@

cppcheck_suppressions:=$(ci_dir)/.cppcheck-suppress
cppcheck_flags:= --quiet --enable=all --error-exitcode=1 \
	--library=$(cppcheck_type_cfg) \
	--suppressions-list=$(cppcheck_suppressions) $(CPPFLAGS)

cppcheck: $(cppcheck_type_cfg)
	@$(CPPCHECK) $(cppcheck_flags) $(_cppcheck_files)

cppcheck-clean:
	@rm -f $(cppcheck_type_cfg)

clean: cppcheck-clean

.PHONY: cppcheck
non_build_targets+=cppcheck cppcheck-clean

define cppcheck
_cppcheck_files+=$1
endef

#############################################################################

misra_ci_dir:=$(ci_dir)/misra
misra_rules:=$(misra_ci_dir)/rules.txt
misra_cppcheck_supressions:=$(misra_ci_dir)/.cppcheck-misra-unused-checks
misra_deviation_suppressions:=$(misra_ci_dir)/.cppcheck-misra-deviations
misra_deviation_suppressions_script:=$(misra_ci_dir)/deviation-suppression.py
misra_suppresions:=$(misra_ci_dir)/.cppcheck-misra-suppressions

misra_dir:=$(root_dir)/misra
misra_deviation_records:=$(misra_dir)/deviations/
misra_deviation_permits:=$(misra_dir)/permits/

define cppcheck_misra_addon
"{\
    \"script\": \"misra\",\
    \"args\": [\
        \"--rule-texts=ci/misra/rules.txt\"\
    ]\
}"
endef

cppcheck_misra_flags:= --quiet --enable=all --error-exitcode=1 \
	--library=$(cppcheck_type_cfg) --addon=$(cppcheck_misra_addon) $(CPPFLAGS) \
	--suppressions-list=$(misra_suppresions)
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
	@$(CPPCHECK) $(cppcheck_misra_flags) $(_misra_c_files)

misra-clean:
	-rm -f $(misra_rules) $(misra_suppresions) $(misra_deviation_suppressions)

$(call ci, yamllint, $(wildcard $(misra_deviation_records) $(misra_deviation_permits)))

clean: misra-clean cppcheck-clean

.PHONY: misra-check misra-clean misra-dev-check
non_build_targets+=misra-check misra-clean

define misra
_misra_c_files+=$1
_misra_h_files+=$2
endef

#############################################################################

ci=$(eval $(call $1, $2, $3, $4, $5, $6, $7, $8, $9))

.PHONY: build
build:

.PHONY: base-ci
base-ci: build cppcheck tidy misra-check
