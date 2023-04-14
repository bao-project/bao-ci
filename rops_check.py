#!/bin/python3

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Bao Project and Contributors. All rights reserved

"""
This script compares the number of ROP (Return-Oriented Programming) gadgets in
two different builds from two branches instances of a Git repository. The script
calls the ROPGadget* tool to do the measurements and outputs the difference in
the number of ROP gadgets between the two provide branches.
* github.com/JonathanSalwan/ROPgadget
"""

import subprocess
import argparse
import sys
import git

# The percentage threshold for the number of ROP gadgets to be accepted.
PERCENTAGE_THRESHOLD = 10

DESCRIPTION = "This script compares the number of ROP (Return-Oriented      \
    Programming) gadgets in two different builds from two branches instances\
    of a Git repository. The script calls the ROPGadget* tool to do         \
    the measurements and outputs the difference in the number of ROP gadgets\
    between the two provide branches. We are assuming that the binary file  \
    is passed in the elf format.                                            \
    * github.com/JonathanSalwan/ROPgadget"

def parse_args():
    """
    This function parses command-line arguments using the argparse module. It
    sets up the argument parser with the specified options and returns the
    parsed arguments.
    """
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("-s", "--source-branch", required=False,
                        help="Name of source branch to compare against (default: current branch)")
    parser.add_argument("-t", "--target-branch", required=False,
                        help="Name of target branch to compare (default: main)")
    parser.add_argument("-b", "--build-cmd", required=True, help="Command to build the repo")
    parser.add_argument("-x", "--exe-path", required=True,
                        help="Path to the executable to measure ROP gadgets in")
    parser.add_argument("-p", "--pct", required=False,
                        help="Percentage threshold for the number of ROP gadgets to be accepted \
                            (default: 10%%)")

    args = parser.parse_args()
    return args

def run_cmd(cmd):
    """
    This function takes a command as input and executes it using the subprocess
    module. It captures the output (stdout) and error (stderr) streams, as well
    as the return code.
    """
    # Run the command using the subprocess module and capture the output, error, and return code.
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                          text=True) as process:

        # Wait for the command to complete and retrieve the output and error streams.
        output, error = process.communicate()

        # Get the return code of the command.
        return_code = process.returncode

    # Return the output, error, and return code as a tuple.
    return output, error, return_code

def measure_rop_gadgets(exe_path):
    """
    This function takes a path to a binary as input and uses the ROPGadget tool
    to measure the number of ROP gadgets in the binary.
    """
    # Run the ROPGadget tool on the binary and capture the output and error streams.
    cmd = f'ROPgadget --binary {exe_path}'
    stdout, stderr, returncode = run_cmd(cmd)

    if returncode != 0:
        raise RuntimeError(f'Error running ROP gadget tool: {stderr}')

    # Search for the "Unique gadgets found:" string
    unique_gadgets_line = None
    for line in stdout.split("\n"):
        if "Unique gadgets found:" in line:
            unique_gadgets_line = line
            break

    # Extract the integer value after the "Unique gadgets found:" string
    unique_gadgets = int(unique_gadgets_line.split(":")[-1].strip())

    return unique_gadgets

def main(pct_threshold):
    """
    This function is the main entry point of the script. It parses command-line
    arguments, measures the number of ROP gadgets in the two branches, and
    prints the difference in the number of ROP gadgets between the two branches.
    """
    args = parse_args()

    repo = git.Repo('.')  # Assumes the current directory is the repository root

    if args.source_branch is None:
        if repo.head.is_detached:
            args.source_branch = repo.git.rev_parse("HEAD", short=True)
        else:
            args.source_branch = repo.active_branch.name

    if args.target_branch is None:
        args.target_branch = 'main'

    # Checkout target branch, build the software, and measure ROP gadgets
    repo.git.checkout(args.target_branch)
    run_cmd(args.build_cmd)
    target_gadgets = measure_rop_gadgets(args.exe_path)

    print(f'Number of ROP gadgets in target branch {args.target_branch}: {target_gadgets}')

    # Checkout source branch, build the software, and measure ROP gadgets
    repo.git.checkout(args.source_branch)
    run_cmd(args.build_cmd)
    source_gadgets = measure_rop_gadgets(args.exe_path)

    print(f'Number of ROP gadgets in source branch {args.source_branch}: {source_gadgets}')

    # Calculate and print the difference in ROP gadgets
    total = source_gadgets - target_gadgets
    percentage = (total / target_gadgets) * 100

    if total > 0:
        print(f'ROP gadgets increased by {total} (+{percentage:.2f}%)')
    elif total < 0:
        print(f'ROP gadgets decreased by {total} ({percentage:.2f}%)')
    else:
        print('ROP gadgets did not change')

    if args.pct is not None:
        pct_threshold = int(args.pct)

    if percentage >= pct_threshold:
        print(f'ERROR: ROP gadgets increased by more than {pct_threshold}%', file=sys.stderr)
        sys.exit(-1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main(PERCENTAGE_THRESHOLD)
