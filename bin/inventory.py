#!/usr/bin/env python3
#
# Script to collect information about an output/results directory
# Support checking of results from simple (count files), to complex (checksums)
#
# 
import argparse
from pathlib import Path
import os, os.path, sys, random, string, time, json
import subprocess
from datetime import datetime

def generate_custom_id():
    timestamp = str(int(time.time()))
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"QW.{timestamp}.{random_chars}"

def du(path):
    """disk usage in human readable format (e.g. '2,1GB')"""
    return subprocess.check_output(['du','-sh', path]).split()[0].decode('utf-8')

def summary_of_storage(path,direc):
    #
    # Call the du to gather storage requirements
    #
    StorageSize = du(path)
    direc.update({"TotalDataSetSize": StorageSize})
    print("TotalDataSetSize",StorageSize)
    return direc

def output_list_of_files(path,direc):
    dirlist = []
    #
    # Print the Directories
    #
    for path, subdirs, files in os.walk(path):
        for filename in files:
            dirlist.append(os.path.join(path, filename))


    # This adds a json element called FileList which is a list of files.
    # These can be further shortened by removing the base dir which is duplicated currently
    direc.update({"FileList": dirlist})
    print(direc)
    #print("Lines In Metadata + FileList:", len(direc) + len(dirlist))
    #print(dirlist)
    return direc

def summary_of_dataset(root,direc):

    #
    # Create path for root directory
    #
    path = Path(root)
    direc.update({"RootPath": root})
    print("RootPath:", root)
    nFiles = sum(1 for x in path.rglob('*') if x.is_file())
    direc.update({"NumFiles": nFiles})
    print("Num of Files:", nFiles)  # Sum Only files, recursive
    nDirsFiles = sum(1 for _ in path.rglob('*'))
    direc.update({"NumDirsFiles": nDirsFiles})
    print("Num of Folders + Files:", nDirsFiles)  # Sum Files and folders, recursive
    return direc


def create_json_metadata(SimID, direc):
    fname = "%s.json" % (SimID)
    with open(fname, "w") as write_file:
        json.dump(direc, write_file, indent=4)


def main():
    parser = argparse.ArgumentParser(
        prog='inventory.py',
        description='A script for managing inventory',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-p', '--path',
        metavar='PATH',
        help='Path relative to location where you invoked script, or absolute path to head of directory tree. Must be one root.'
    )

    parser.add_argument(
        '-u', '--usage',
        action='store_true',
        help='Retrieve summary usage information of tree and files.'
    )

    parser.add_argument(
        '-d', '--direct',
        action='store_true',
        help='Output list of files in dataset.'
    )

    parser.add_argument(
        '-s', '--summary',
        action='store_true',
        help='Summary of dataset number of files, number of directories.'
    )

    parser.add_argument(
        '-a', '--all',
        action='store_true',
        help='Prints -s -u -d in that order.'
    )

    parser.add_argument(
        '-j', '--json',
        metavar='PATH',
        help='Output a simID.json metadata file about the dataset.'
    )

    args = parser.parse_args()

    #
    # Assemble the metadata file this sim.
    #
    dirdict = {}

    SimID = generate_custom_id()
    dirdict.update({"SimID": SimID})
    print("SimID:", SimID)

    #
    # Collect Time Information
    #
    # Getting the current date and time
    dt = datetime.now()
    iso_date = dt.isoformat()
    print('CreationDate:', iso_date)
    dirdict.update({"CreationDate": iso_date})

    # getting the timestamp
    ts = datetime.timestamp(dt)
    dirdict.update({"Timestamp": ts})
    print("Timestamp:", ts)

    # Check for the path to use as the root. Use current directory as default
    if args.path:
        root = args.path
    else:
        root = os.getcwd()

    #if args.summary or args.all:
    dirdict = summary_of_dataset(root,dirdict)

    #if args.usage or args.all:
    dirdict = summary_of_storage(root,dirdict)

    #if args.direct or args.all:
    dirdict = output_list_of_files(root,dirdict)

    if args.json:
        print("DataSetRootDir:",args.json)
        create_json_metadata(SimID,dirdict)

if __name__ == '__main__':
    main()
