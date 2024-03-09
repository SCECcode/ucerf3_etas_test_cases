#!/usr/bin/env python3

#
# Script to collect information about an output/results directory
# Support checking of results from simple (count files), to complex (checksums)
#
# 
from pathlib import Path
import os, os.path, sys, random, string, time, json
import subprocess
from datetime import datetime


def generate_custom_id():
    timestamp = str(int(time.time()))
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"QW.{timestamp}.{random_chars}"

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

def du(path):
    """disk usage in human readable format (e.g. '2,1GB')"""
    return subprocess.check_output(['du','-sh', path]).split()[0].decode('utf-8')
#
# ToDo:
# Count different aspects of the input directory using command line parameters
# -f # of files
# -d # of files + directories

nvals = len(sys.argv)

if nvals < 2: 
  root = "."
else:
  root = sys.argv[1]

#
# Assemble the metadata file this sim.
#
dirdict = {}

SimID = generate_custom_id()
dirdict.update({"SimID":SimID})
print("SimID:",SimID)

#
# Collect Time Information
#
# Getting the current date and time
dt = datetime.now()
iso_date = dt.isoformat()
print('CreationDate:', iso_date)
dirdict.update({"CreationDate":iso_date})

# getting the timestamp
ts = datetime.timestamp(dt)
dirdict.update({"Timestamp":ts})
print("Timestamp:", ts)

#
# Create path for root directory
#
path = Path(root)
dirdict.update({"RootPath":root})
print("RootPath:",root)
nFiles=sum(1 for x in path.rglob('*') if x.is_file())
dirdict.update({"NumFiles":nFiles})
print("Num of Files:",sum(1 for x in path.rglob('*') if x.is_file()))  # Only files, recursive
nDirsFiles  = sum(1 for _ in path.rglob('*'))
dirdict.update({"NumDirsFiles":nDirsFiles})
print("Num of Folders + Files:", sum(1 for _ in path.rglob('*')))  # Files and folders, recursive
StorageSize = du(root)
dirdict.update({"TotalDirSize":StorageSize})
print("TotalDirSize:",du(root))
#
# print the Metadata so far
#
print(dirdict)

#
# Create a list of tuples. They all have the same ID, so they collide in a dict
#
# "FileName":<filename>

dirlist = []
#
# Print the Directories
#
for path, subdirs, files in os.walk(root):
    for filename in files:
        dirlist.append(os.path.join(path, filename))


# This adds a json element called FileList which is a list of files.
# These can be further shortened by removing the base dir which is duplicated currently
dirdict.update({"FileList":dirlist})

print("Lines In Metadata",len(dirdict))

fname = "%s.json"%(SimID)
with open(fname, "w") as write_file:
    json.dump(dirdict, write_file, indent = 4)

print("Completed")
