#!/bin/python3

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Bao Project and Contributors. All rights reserved

"""
Provides spell checking functionality to various filetypes
"""

import os
import sys
import argparse
import yaml
from spellchecker import SpellChecker

spell = SpellChecker()

def spelling(text):

    """ Perform spelling check to a string of text """

    words = spell.split_words(text)
    misspelled = spell.unknown(words)

    misspelled = [x for x in misspelled if x.strip() and x]
    return misspelled

def parse_args():

    """ Decode script parameters """

    parser = argparse.ArgumentParser(
            description="Process different file types with specific options")
    parser.add_argument("-t", "--type", choices=["txt", "yaml"], required=True, \
                        help="File type (currently supports 'txt', 'yaml')")
    parser.add_argument("-k", "--keys", nargs="+",
                        help=
                        "List of YAML fields (only applicable for YAML files)")
    parser.add_argument("-f", "--files", nargs="+", required=True,
                        help="List of input file paths")
    parser.add_argument("-d", "--dictionaries", nargs="+",
                        help="List of dictionary files")

    args = parser.parse_args()
    return args

def process_yaml_file(file_path, keys):

    """ Process a single yaml file """

    with open(file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
        for key in keys:
            if not key in data:
                sys.exit(f"Error parsing yaml file: Key {key} not found")

            misspellings = spelling(data[key])
            if len(misspellings) > 0:
                print(f"Misspellings in {file_path} in \"{key}\":")
                for misspelling in misspellings:
                    print(f"\t{misspelling}")

def process_yaml_files(file_paths, keys=None):

    """ Process a list of yaml files """

    if keys:
        for file_path in file_paths:
            process_yaml_file(file_path, keys)
    else:
        sys.exit("Error parsing yaml file: key(s) not provided")

def process_txt_file(file_path):

    """ Process a single text files """

    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()
        misspellings = spelling(data)
        if len(misspellings) > 0:
            print(f"Misspellings in {file_path}:")
            for misspelling in misspellings:
                print(f"\t{misspelling}")

def process_txt_files(file_paths):

    """ Process a list of text files """

    for file_path in file_paths:
        process_txt_file(file_path)

def main():

    """
    Parse arguments, and check spelling of the provided files
    """

    args = parse_args()
    dictionaries = ["./dictionary.txt"]

    if args.dictionaries is not None:
        dictionaries = args.dictionaries
    else:
        if not os.path.exists(dictionaries[0]):
            print(f"Default dictionary {dictionaries[0]} does not exist.",
                  file=sys.stderr)
            print("Consider using the ci provided dictionary using \"-d" \
                  "ci/dictionary.txt\"", file=sys.stderr)
            sys.exit(-1)

    for dictionary in dictionaries:
        spell.word_frequency.load_text_file(dictionary)

    if args.type == "txt":
        process_txt_files(args.files)
    elif args.type == "yaml":
        if args.keys is not None:
            process_yaml_files(args.files, args.keys)
        else:
            process_yaml_files(args.files)
    else:
        print("Invalid file type")

if __name__ == "__main__":
    main()
