#!/bin/python3

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Bao Project and Contributors. All rights reserved

"""
Generating HIS metrics check
"""

import sys
import argparse
import os

CYCLOMATIC_TRESHOLD = 10

def process_metrics(filename):

    """Process each HIS metric."""

    metric_fail = 0
    metric_fail += process_complexity(filename)
    return metric_fail

def process_complexity(file):

    """Process McCabe Cyclomatic Complexity for each function in a file"""

    metric_fail = 0
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
            metric_fail = 1
    return metric_fail

if __name__ == "__main__":
    CHECK_FAIL = 0
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("files", nargs="+", help="The files to process")
    ARGS = PARSER.parse_args()

    for file_path in ARGS.files:
        CHECK_FAIL += process_metrics(file_path)

    if CHECK_FAIL:
        sys.exit(-1)
