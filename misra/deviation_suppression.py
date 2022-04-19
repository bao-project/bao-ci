#!/usr/bin/python3

"""
Generating MISRA checker input files for deviation suppresions.
"""

import sys
import re
import os

def eprint(*args, **kwargs):

    """Print to stderr."""

    print(*args, file=sys.stderr, **kwargs)

MISRA_DEV_REGEX=r"MISRA(DEV(FILE|END|START)?|FP):(,?R([\.\d]*))+:(,?(MDP|MDR)(\d*))*"

def print_suppression(file_name, rule, line=None, is_range=False):

    """Print the suppression for the rule in cppcheck format."""

    if line is not None:
        print(f'misra-c2012-{rule}:{file_name}:{line}')
        print(f'unmatchedSuppression:{file_name}:{line}')
    else:
        print(f'misra-c2012-{rule}:{file_name}')

def filter_annotations(file_name):

    """Generatates the filtered misra annotations for a file"""

    file = open(file_name)
    for lineno, line in enumerate(file):
        match = re.search(MISRA_DEV_REGEX, line)
        if match is None:
            continue
        (start, end) = match.span()
        yield (lineno, line[start:end])

def process_deviations(file_name):

    """Process each annotation and suppress it if valid."""

    dev_starts = []
    for lineno, annotation in filter_annotations(file_name):
        [header, rules, deviations] = annotation.split(':')
        tag = rules + deviations
        rule_array = [rule[1:] for rule in rules.split(',')]
        lineno += 1
        if header == 'MISRADEVSTART':
            dev_starts.append((rules, lineno, tag))
        elif header == 'MISRADEVEND':
            if not dev_starts:
                eprint(f'No matching MISRADEVSTART for \'{annotation}\' at \
                    {file_name}:{lineno}')
                sys.exit(-1)
            (rules, startline, starttag) = dev_starts.pop()
            if starttag != tag:
                eprint(f'\'{annotation}\' at {file_name}:{lineno}, does not \
                    match previous MISRADEVSTART')
                sys.exit(-1)
            for rule in rule_array:
                for loc in range(startline, lineno):
                    print_suppression(file_name, rule, loc, True)
        elif header == 'MISRADEVFILE':
            for rule in rule_array:
                print_suppression(file_name, rule)
        else:
            for rule in rule_array:
                print_suppression(file_name, rule, lineno+1)
    if dev_starts:
        (rules, startline, starttag) = dev_starts.pop()
        eprint(f'No MISRADEVEND for MISRADEVSTART ad at {file_name}:{startline}')
        sys.exit(-1)

if __name__ == "__main__" :
    for arg in sys.argv[1:]:
        process_deviations(os.path.realpath(arg))
