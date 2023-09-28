# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Bao Project and Contributors. All rights reserved

# Check if a given variable is defined.
# @param variable name
# @param error message (optional)
# @example $(call check_variable_defined, XPTO, "The XPTO must be defined!")
define check_variable_defined
$(if $($(strip $1)),,$(error $(strip $1) not defined: $(strip $2)))
endef

# Check if a variable is a valid directory path.
# Returns nothing if false, some unknown value if true.
# @param directory path (can be absolute or relative)
# @example $(call is_dir, src/core)
define is_dir
$(strip $(wildcard $1/.))
endef

# Check if a variable is a valid file path (not a directory).
# Returns nothing if false, some unknown value if true.
# @param file path (absolute of relative)
# @example $(call is_dir, src/core/init.c)
define is_file
$(if $(strip $(wildcard $1/.)),,$1,)
endef

# List files within a directory that match a wildcard pattern
# @param directory path (can be absolte of relative)
# @param a make wildcard pattern for the files' name (no relative paths)
# example $(call list_dir, src, *.c)
define list_dir_files
$(strip \
	$(foreach node, $(wildcard $(strip $1)/$(strip $2)), \
		$(if $(call is_file, $(node)),$(node))) \
)
endef

# List files within a directory and all of its subdirectories which names 
# matches a wildcard pattern
# @param directory path (can be absolute of relative)
# @param a make wildcard pattern for files' name (no relative paths)
# example $(call list_dir_files_recursive, src, *.c)
define list_dir_files_recursive
$(strip \
	$(call list_dir_files, $1, $2) \
	$(foreach node, $(wildcard $(strip $1)/*), \
		$(if $(call is_dir, $(node)), 	
			$(call list_dir_files_recursive, $(node), $(strip $2)))) \
)
endef
