#!/bin/python3

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Bao Project and Contributors. All rights reserved

"""
Generating HIS metrics check
"""

import sys
import argparse

if __name__ == "__main__":
    METRICS_LIST = []
    CHECK_FAIL = 0
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("files", nargs="+", help="The files to process")
    ARGS = PARSER.parse_args()

    for metric in METRICS_LIST:
        CHECK_FAIL += metric(ARGS)

    if CHECK_FAIL:
        sys.exit(-1)
