#!/bin/python3

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Bao Project and Contributors. All rights reserved

"""
Generating HIS metrics check
"""

import sys
import argparse
import os
from anytree import Node

def traverse(node, threshold, failed_nodes=None):
    """
    Helper function to traverse the tree create in the process_calls function
    """
    if failed_nodes is None:
        failed_nodes = []

    # Initialize a variable to True. This will remain True if all checks pass.
    is_new_node = True

    # Check each node in failed_nodes
    for f_node in failed_nodes:
        # If the current node's name is the same as a name in failed_nodes
        if node.name == f_node.name:
            # Set is_new_node to False and break the loop
            is_new_node = False
            break

    # If the node has more children than the threshold and is_new_node is still True
    if len(node.children) > threshold and is_new_node:
        # Add the node to failed_nodes
        failed_nodes.append(node)

    # For each child of the current node
    for child in node.children:
        # Recursively traverse the child's subtree, passing the current list of nodes
        traverse(child, threshold, failed_nodes)


    return failed_nodes

def process_calling(files, threshold):
    """
    Process the calling metric
    """
    print(f"Processing CALLING metric with threshold [0-{threshold}] for files: \
          {', '.join(files)}")

    return 0

def process_calls(files, threshold):
    """
    Process the number of called functions. This function checks the number of functions does a
    particular function calls. If the number of 'calls' in a function exceeds the defined
    threshold, an error message is printed and the error count is incremented.

    Args:
        files: A list of file paths to check for 'calls'.
        threshold: The maximum number of permitted 'calls' in a function.

    Returns:
        The number of files that exceed the number of 'calls'.
    """

    metric_fail = 0
    nodes = {}
    root = None

    print("--------------------------------------------")
    print(f"Processing CALLS metric with threshold [0-{threshold}]")
    print("--------------------------------------------")

    # Process each file
    for file in files:
        # Run 'cflow' on the file and split the output into lines
        lines = os.popen(f"cflow -l {file}").read().split('\n')

        trees = []
        for line in lines:

            if not line.strip():
                continue  # Skip empty lines

            # Extract level and func/file name
            lvl, descriptor = line.split('}', 1)
            lvl = int(lvl.strip('{').strip())

            # Create root node or child node based on level
            if lvl == 0:
                root = Node(descriptor)  # Create a new root node
                trees.append(root)
                nodes = {0: root}  # Reset nodes dictionary for the new tree
            else:
                parent = nodes[lvl - 1]
                # Update the current node and its parent reference
                nodes[lvl] = Node(descriptor, parent=parent)

        # Check the number of calls in each tree
        for root in trees:
            nodes_failed = traverse(root, threshold)
            for node in nodes_failed:
                func_name = node.name.split(')', 1)[0].strip() + ')'
                print(f"At {file} has {len(node.children)} calls in function {func_name}")
                metric_fail += 1

    return metric_fail


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
