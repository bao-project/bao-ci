# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Bao Project and Contributors. All rights reserved

"""
Generating HIS metrics check
"""

import os
import sys

CYCLOMATIC_TRESHOLD = 10
COMMENT_DENSITY = 0.2
GOTO_TRESHOLD = 0
CALL_TRESHOLD = 7
CALLEE_TRESHOLD = 5
STATEMENTS_TRESHOLD = 50
METRIC_FAIL = 0

def process_metrics(filename):

    """Process each HIS metric."""

    process_complexity(filename)
    total_stmt = process_statements(filename)
    process_comments(filename, total_stmt)
    process_callees(filename)
    process_goto(filename)
    process_calls(filename)

def process_complexity(file):

    """Process McCabe Cyclomatic Complexity for each function in a file"""

    global METRIC_FAIL
    complexity = "pmccabe -c "
    lines = os.popen(complexity + str(file))
    lines = lines.read()
    sline = lines.split('\n')

    for num in range(len(sline)-1):
        fields = sline[num].split('\t')
        colony_count = int(fields[0])
        if colony_count > CYCLOMATIC_TRESHOLD:
            print("Complexity exceeded (max." + str(CYCLOMATIC_TRESHOLD) + "): "
                  + fields[0] + " at " + fields[5])
            METRIC_FAIL = 1

def process_statements(file):

    """Process number of statements in a function"""

    global METRIC_FAIL
    total_stmt = 0
    complexity = "pmccabe -c "
    lines = os.popen(complexity + str(file))
    lines = lines.read()
    sline = lines.split('\n')

    for num in range(len(sline)-1):
        fields = sline[num].split('\t')
        num_statements = int(fields[2])
        total_stmt += num_statements
        if num_statements > STATEMENTS_TRESHOLD:
            function = fields[5].split(':')
            print(str(function[1]) + " exceeded the # of statements allowed with "
                  + fields[2] + " statements (max. " + str(STATEMENTS_TRESHOLD) +
                  ")" + " at " + str(function[0]))
            METRIC_FAIL = 1
    return total_stmt

def process_comments(file, total_stmt):

    """Process comment density in a file"""

    global METRIC_FAIL
    lines = os.popen("pygount  --format=cloc-xml " + str(file))
    lines = lines.read()
    sline = lines.split(' ')
    for num in range(len(sline)-1):
        if sline[num].startswith("comment"):
            comf = sline[num].split("=")
            comf = int(comf[1].strip('"'))/total_stmt
            if comf < 0.2:
                print("Comment density (comments/statements) must be bigger \
than 0.2! Current value is " + str(comf))
                METRIC_FAIL = 1
            break

def process_goto(file):

    """Process number of go to statements"""

    global METRIC_FAIL
    qmcalc = "qmcalc "
    lines = os.popen(qmcalc + str(file))
    lines = lines.read()
    sline = lines.split('\n')

    for num in range(len(sline)-1):
        fields = sline[num].split('\t')
        if int(fields[18]) > GOTO_TRESHOLD:
            print("Illegal goto expression in a function in" + file)
            METRIC_FAIL = 1

def process_calls(file):

    """Process number of calls inside a function"""

    global METRIC_FAIL
    cflow = "cflow -l --depth=2 "
    if file.endswith(".c"):
        lines = os.popen(cflow + str(file))
        lines = lines.read()
        sline = lines.split('\n')
        call_counter = 0

        for num in range(len(sline)-1):
            fields = sline[num].split('\t')
            fields = fields[0].split('}')
            fields[0] = fields[0].lstrip("{")
            fields[0] = fields[0].lstrip()
            fields[1] = fields[1].lstrip()

            if (int(fields[0]) == 0 and call_counter > CALL_TRESHOLD):
                print("With " + str(call_counter) + " calls (of a maximum "
                      + str(CALL_TRESHOLD) + "): " + parent_func)
                METRIC_FAIL = 1

            if int(fields[0]) == 0:
                parent_func = fields[1]
                call_counter = 0

            if int(fields[0]) > 0:
                call_counter = call_counter + 1

def process_callees(file):

    """Process number of times a function is called in a file"""

    global METRIC_FAIL
    cflow = "cflow -r -l --depth=2 "
    if file.endswith(".c"):
        lines = os.popen(cflow + str(file))
        lines = lines.read()
        sline = lines.split('\n')
        callee_counter = 0

        for num in range(len(sline)-1):
            fields = sline[num].split('\t')
            fields = fields[0].split('}')
            fields[0] = fields[0].lstrip("{")
            fields[0] = fields[0].lstrip()
            fields[1] = fields[1].lstrip()

            if (int(fields[0]) == 0 and callee_counter > CALLEE_TRESHOLD):
                print(parent_func + " is being called " + str(callee_counter) +
                      " times (from a maximum of " + str(CALLEE_TRESHOLD) +
                      ")" + " in " + file)
                METRIC_FAIL = 1

            if int(fields[0]) == 0:
                parent_func = fields[1]
                callee_counter = 0

            if int(fields[0]) > 0:
                callee_counter = callee_counter + 1

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        process_metrics(os.path.realpath(arg))

    if METRIC_FAIL:
        sys.exit(-1)
