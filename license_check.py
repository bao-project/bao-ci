#!/bin/python3

"""
Check for SPDX license headers in source files
"""

import sys
import re
import argparse
import license_expression

def eprint(*args, **kwargs):

    """Print to stderr."""

    print(*args, file=sys.stderr, **kwargs)

SPDX_PARSER = None
# TODO: improve regex to support multiple licenses (AND, OR) and execeptions (WITH)
SPDX_REGEX = r'SPDX-License-Identifier: \(?(?P<license_expr>\S*)\)?'

def check_license(filename, spdx_expr):

    """Check if 'filename' has a SPDX identifier complying with 'spdx_exr'"""

    try:
        file = open(filename)
    except FileNotFoundError:
        eprint(f'Can\'t open file \'{filename}\'')
        return False

    for line in file:

        if line.strip() == '':
            continue

        # allow not in first line in case of scripts
        if  line.startswith('#!'):
            continue

        match = re.search(SPDX_REGEX, line)
        if match is not None:
            license_expr_str = match.groupdict()['license_expr']
            spdx_parser = license_expression.get_spdx_licensing()
            license_expr_info = spdx_parser.validate(license_expr_str)
            if license_expr_info.errors:
                eprint(f'Invalid SPDX expression in \'{filename}\':')
                for err in license_expr_info.errors:
                    eprint('\t' + err)
                return False
            license_expr = spdx_parser.parse(license_expr_str)

            if not spdx_parser.contains(spdx_expr, license_expr):
                eprint(f'\'{license_expr_str}\' in \'{filename}\' ' \
                    f'does not comply with supplied SPDX expression \'{spdx_expr}\'')
                return False

            return True

    eprint(f'License not found in {filename}')
    return False


def main():

    """
    main function parses arguments, initializes the spdx expression and calls
    check license on each source file
    """

    parser = argparse.ArgumentParser(description='Check for SPDX ID in source files')
    parser.add_argument('-l', '--license', metavar='license',
        help='SPDX expression describing allowed licenses')
    parser.add_argument('file', metavar='file', nargs='+',
        help='Source files to be checked for license')
    args = parser.parse_args()

    spdx_parser = license_expression.get_spdx_licensing()
    spdx_expr = args.license
    if not spdx_expr:
        spdx_expr = 'Apache-2.0'
        eprint(f'No SPDX expression supplied. Using {spdx_expr}.')
    spdx_expr_info = spdx_parser.validate(spdx_expr)
    if spdx_expr_info.errors:
        eprint('Invalid supplied SPDX expression\':')
        for err in spdx_expr_info.errors:
            eprint('\t' + err)
        return
    spdx_expr = spdx_parser.parse(spdx_expr)

    success = True
    for file in args.file:
        success = check_license(file, spdx_expr) and success

    if not success:
        sys.exit(-1)

if __name__ == "__main__":
    main()
