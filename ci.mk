CPPCHECK?=cppcheck
CLANG_VERSION?=12
CLANG-FORMAT?=clang-format-$(CLANG_VERSION)
CLANG-TIDY?=clang-tidy-$(CLANG_VERSION)

#############################################################################

define format
format:
	@$(CLANG-FORMAT) --style=file -i $1
format-check:
	@diff <(cat $1) <($(CLANG-FORMAT) --style=file $1)
endef

#############################################################################

define tidy
tidy:
	@$(CLANG-TIDY) $1 -- --target=$(clang-arch) $(CPPFLAGS)
endef

#############################################################################

cppcheck_flags:= --quiet --enable=all --error-exitcode=1 $(CPPFLAGS)
std_incs:=$(shell $(CROSS_COMPILE)gcc -E -Wp,-v -xc /dev/null 2>&1 | grep "^ ")

define cppcheck
cppcheck:
	@$(CPPCHECK) $(cppcheck_flags) $(addprefix -I , $(std_incs)) $1
endef

#############################################################################

ci-rule=$(eval $(call $1, $2, $3, $4, $5, $6, $7, $8, $9))
