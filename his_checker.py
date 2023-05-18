#!/bin/python3

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Bao Project and Contributors. All rights reserved

"""
Generating HIS metrics check
"""

import sys
import argparse

METRIC_FAIL = 0

def process_metrics(filename):

    """Process each HIS metric."""
    print(filename)

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("files", nargs="+", help="The files to process")
    ARGS = PARSER.parse_args()

    for file_path in ARGS.files:
        process_metrics(file_path)

    if METRIC_FAIL:
        sys.exit(-1)
