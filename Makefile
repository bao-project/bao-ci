root_dir:=$(realpath .)
ci_dir:=$(root_dir)

all:

include ci.mk

python_scripts:= \
	$(root_dir)/misra/deviation_suppression.py \
	$(root_dir)/license_check.py
$(call ci, pylint, $(python_scripts))

yaml_files:= \
	$(root_dir)/misra/deviation_record_template.yml \
	$(root_dir)/misra/deviation_permit_template.yml
$(call ci, yamllint, $(yaml_files))

ci: license pylint yamllint
