#!/usr/bin/python3

import sys
import re
import os

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

MISRA_DEV_REGEX="MISRA(DEV(FILE|END|START)?|FP):(,?R([\.\d]*))+:(,?(MDP|MDR)(\d*))*"

def print_deviation(file_name, rule, line=None, is_range=False):
    if line is not None:
        print(f'misra-c2012-{rule}:{file_name}:{line}')
        if is_range:
            print(f'unmatchedSuppression:{file_name}:{line}')
    else:
        print(f'misra-c2012-{rule}:{file_name}')

def process_deviations(file_name):
    file_name = os.path.realpath(file_name)
    file = open(file_name)
    dev_starts = []
    for lineno, line in enumerate(file):
        match = re.search(MISRA_DEV_REGEX, line)
        if match is None:
            continue
        (s, e) = match.span()
        matched_str = line[s:e]
        [header, rules, deviations] = matched_str.split(':')
        tag = rules + deviations
        rule_array = [rule[1:] for rule in rules.split(',')]
        lineno += 1
        if header == 'MISRADEVSTART':
            dev_starts.append((rules, lineno, tag))
        elif header == 'MISRADEVEND':
            if not dev_starts:
                eprint(f'No matching MISRADEVSTART for \'{matched_str}\' at {file_name}:{lineno}')
                sys.exit(-1)
            (rules, startline, starttag) = dev_starts.pop()
            if starttag != tag:
                eprint(f'\'{matched_str}\' at {file_name}:{lineno}, does not match previous MISRADEVSTART')
                sys.exit(-1)
            for rule in rule_array:
                for line in range(startline, lineno):
                    print_deviation(file_name, rule, line, True)
        elif header == 'MISRADEVFILE':
            for rule in rule_array:
                print_deviation(file_name, rule)
        else:
            for rule in rule_array:
                print_deviation(file_name, rule, lineno+1)
    if dev_starts:
        (rules, startline, starttag) = dev_starts.pop()
        eprint('No MISRADEVEND for MISRADEVSTART ad at {file_name}:{startline}')
        exit(-1)

if __name__ == "__main__" :
    for file_name in sys.argv[1:]:
        process_deviations(file_name)



