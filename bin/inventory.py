#!/usr/bin/env python3

#
# Script to collect information about an output/results directory
# Support checking of results from simple (count files), to complex (checksums)
#
# 
from pathlib import Path
import os, os.path, sys

def get_file_sizes(root_dir):
    file_sizes = {}
    with os.scandir(root_dir) as entries:
        for entry in entries:
            if entry.is_file():
                file_sizes[entry.name] = entry.stat().st_size
    return file_sizes

def format_size(size):
    for uni in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.2f} {uni}"

def print_file_sizes(root_dir):
    file_sizes = get_file_sizes(root_dir)
    for file, size in file_sizes.items():
        formatted_size = format_size(size)
        print(f"{file}: {formatted_size}")

#
# Count different aspects of the input directory using command line parameters
# -f # of files
# -d # of files + directories

#print(f"Name of the script      : {sys.argv[0]=}")
#print(f"Arguments of the script : {sys.argv[1:]=}")

nvals = len(sys.argv)

if nvals < 2: 
  root = "."
else:
  root = sys.argv[1]

#
#
#
path = Path(root)
print("RootDir:",path)
print("Num of Folders + Files:", sum(1 for _ in path.rglob('*')))  # Files and folders, recursive
print("Num of Files:",sum(1 for x in path.rglob('*') if x.is_file()))  # Only files, recursive
print("FileSizes:",root)
print_file_sizes(root)
#
# Print the Directories
#
for path, subdirs, files in os.walk(root):
    for filename in files:
        print(os.path.join(path, filename))
