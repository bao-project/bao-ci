# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Bao Project and Contributors. All rights reserved

# Check if a given variable is defined.
# @param variable name
# @param error message (optional)
# @example $(call check_variable_defined, XPTO, "The XPTO must be defined!")
define check_variable_defined
$(if $($(strip $1)),,$(error $(strip $1) not defined: $(strip $2)))
endef
