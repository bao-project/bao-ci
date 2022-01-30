ci_dir:=$(realpath ci)

CPPCHECK?=cppcheck
CLANG_VERSION?=12
CLANG-FORMAT?=clang-format-$(CLANG_VERSION)
CLANG-TIDY?=clang-tidy-$(CLANG_VERSION)

#############################################################################

clang_format_flags:=--style=file
format_file:=$(root_dir)/.clang-format
original_format_file:=$(ci_dir)/.clang-format

define format
$(format_file): $(original_format_file)
	@cp $$< $$@

format: $(format_file)
	@$(CLANG-FORMAT) $(clang_format_flags) -i $1

format-check: $(format_file)
	@diff <(cat $1) <($(CLANG-FORMAT) $(clang_format_flags) $1)

format-clean:
	-@rm -f $(format_file)

clean: format-clean

.PHONY: format format-check format-clean
non_build_targets+=format format-check format-clean
endef

#############################################################################

define tidy
tidy:
	@$(CLANG-TIDY) --config-file=$(ci_dir)/.clang-tidy $1 -- \
		--target=$(clang-arch) $(CPPFLAGS) 2> /dev/null

.PHONY: tidy
non_build_targets+=tidy
endef

#############################################################################

cppcheck_suppressions:=$(ci_dir)/.cppcheck-suppress
cppcheck_flags:= --quiet --enable=all  --error-exitcode=1 \
	--suppressions-list=$(cppcheck_suppressions) $(CPPFLAGS)
std_incs:=$(shell $(CROSS_COMPILE)gcc -E -Wp,-v -xc /dev/null 2>&1 | grep "^ ")

define cppcheck
cppcheck:
	@$(CPPCHECK) $(cppcheck_flags) $(addprefix -I , $(std_incs)) $1

.PHONY: cppcheck
non_build_targets+=cppcheck
endef

#############################################################################

misra_dir:=$(ci_dir)/misra
misra_rules:=$(misra_dir)/rules.txt
cppcheck_misra_addon:=$(misra_dir)/misra.json
cppcheck_misra_flags:= --quiet --suppress=all --error-exitcode=1 --addon=$(cppcheck_misra_addon) $(CPPFLAGS)
zephyr_coding_guidelines:=https://raw.githubusercontent.com/zephyrproject-rtos/zephyr/main/doc/contribute/coding_guidelines/index.rst

ifeq ($(MISRA_C2012_GUIDELINES),)
$(misra_rules):
	@echo "Appendix A Summary of guidelines" > $@
	-@wget -q -O - $(zephyr_coding_guidelines) | grep "\* -  Rule" -A 2 | sed -n '2~2!s/\(.\{9\}\)//p' >> $@
else
$(misra_rules):
	@pdftotext $(MISRA_C2012_GUIDELINES) $@
endif

define misra
misra-check: $(misra_rules)
	@$(CPPCHECK) $(cppcheck_misra_flags) $1

misra-clean:
	-rm -f $(misra_rules)
	-find . -name "*.dump" | xargs rm -f

clean: misra-clean

.PHONY: misra-check misra-clean
non_build_targets+=misra-check misra-clean
endef

#############################################################################

ci-rule=$(eval $(call $1, $2, $3, $4, $5, $6, $7, $8, $9))
