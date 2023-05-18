<<<<<<< HEAD
#!/bin/python3

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Bao Project and Contributors. All rights reserved

"""
Generating HIS metrics check
"""

import sys
import argparse

def process_calling(files, threshold):
    """
    Process the calling metric
    """
    print(f"Processing CALLING metric with threshold [0-{threshold}] for files: \
          {', '.join(files)}")

    return 0

def process_calls(files, threshold):
    """
    Process the calls metric
    """

    print(f"Processing CALLS metric with threshold [0-{threshold}] for files: {', '.join(files)}")

    return 0

def process_comf(files, threshold):
    """
    Process the comf metric
    """

    print(f"Processing COMF metric with threshold >{threshold} for files: {', '.join(files)}")

    return 0

def process_goto(files, threshold):
    """
    Process the goto metric
    """

    print(f"Processing GOTO metric with threshold {threshold} for files: {', '.join(files)}")

    return 0

def process_level(files, threshold):
    """
    Process the level metric
    """

    print(f"Processing LEVEL metric with threshold [0-{threshold}] for files: {', '.join(files)}")

    return 0

def process_param(files, threshold):
    """
    Process the parameters metric
    """

    print(f"Processing PARAMETERS metric with threshold [0-{threshold}] for files: \
          {', '.join(files)}")

    return 0

def process_path(files, threshold):
    """
    Process the path metric
    """

    print(f"Processing PATH metric with threshold [1-{threshold}] for files: {', '.join(files)}")

    return 0

def process_return(files, threshold):
    """
    Process the return metric
    """

    print(f"Processing RETURN metric with threshold [0-{threshold}] for files: {', '.join(files)}")

    return 0

def process_stmt(files, threshold):
    """
    Process the stmt metric
    """

    print(f"Processing STMT metric with threshold [1-{threshold}] for files: {', '.join(files)}")

    return 0

def process_vocf(files, threshold):
    """
    Process the vocf metric
    """
    print(f"Processing VOCF metric with threshold [1-{threshold}] for files: {', '.join(files)}")

    return 0

def process_ap_cg_cycle(files, threshold):
    """
    Process the ap_cg_cycle metric
    """

    print(f"Processing AP_CG_CYCLE metric with threshold {threshold}] for files: \
          {', '.join(files)}")

    return 0

def process_v_g(files, threshold):
    """
    Process the v_g metric
    """

    print(f"Processing V_G metric with threshold [1-{threshold}] for files: {', '.join(files)}")

    return 0

# Define the list of available metrics, their corresponding functions, and their default thresholds
METRICS = {
    'calling' : {
        'function': process_calling,
        'threshold': 5,
    },
    'calls': {
        'function': process_calls,
        'threshold': 7,
    },
    'comf': {
        'function': process_comf,
        'threshold': 0.2,
    },
    'goto': {
        'function': process_goto,
        'threshold': 0,
    },
    'level': {
        'function': process_level,
        'threshold': 4,
    },
    'param': {
        'function': process_param,
        'threshold': 5,
    },
    'path': {
        'function': process_path,
        'threshold': 80,
    },
    'return': {
        'function': process_return,
        'threshold': 1,
    },
    'stmt': {
        'function': process_stmt,
        'threshold': 50,
    },
    'vocf': {
        'function': process_vocf,
        'threshold': 4,
    },
    'ap_cg_cycle': {
        'function': process_ap_cg_cycle,
        'threshold': 0,
    },
    'v_g': {
        'function': process_v_g,
        'threshold': 10,
    },
}

if __name__ == "__main__":
    CHECK_FAIL = 0

    # Define the command-line argument parser
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("-f", "--files", nargs="+", help="The files to process", required=True)

    # Add an argument for each metric
    for metric, metric_info in METRICS.items():
        PARSER.add_argument(f"--{metric}", type=int, default=metric_info['threshold'],
                            help=f"Enable {metric} and specify its threshold", metavar="THRESHOLD")

    PARSER.add_argument("-e", "--exclude", nargs="*", default=[], help="The metrics to exclude")

    ARGS = PARSER.parse_args()

    # Verify that the excluded metrics are valid
    for metric in ARGS.exclude:
        if metric not in METRICS:  # iterate over dictionary directly
            print(f"Invalid metric {metric} specified in --exclude")
            print(f"Valid metrics are: {', '.join(METRICS)}")  # iterate over dictionary directly
            sys.exit(-1)

    # Process each metric
    for metric, metric_item in METRICS.items():
        # Check if the metric is excluded
        if metric in ARGS.exclude:
            continue

        # Get the function and threshold for the metric
        metric_function = metric_item['function']
        val = getattr(ARGS, metric)

        # Add the number of failures for the metric to the total failure count
        CHECK_FAIL += metric_function(ARGS.files, val)
        print("--------------------------------------------")
        if CHECK_FAIL:
            print(f"{metric.upper()} metric failed with {CHECK_FAIL} error(s)\n")
        else:
            print(f"{metric.upper()} metric passed")

    # If there were any failures, exit with an error code
    if CHECK_FAIL:
        sys.exit(-1)
=======

# wip
>>>>>>> 99e561e (feat(HIS): add HIS script into makefile python scripts)
