#!/usr/bin/python3

"""A script for resizing images to specified maximum dimensions

Uses "convert" utility of the ImageMagick suite of tools, which thus must be installed

@author: Frantisek Hajnovic
@email: ferohajnovic@gmail.com
"""

# ---------------------------------------------------------------
# Imports
# ---------------------------------------------------------------

import getopt
import sys
import os
import re
import subprocess

# ---------------------------------------------------------------
# Constants
# ---------------------------------------------------------------

SEPARATOR = '-----'

# ---------------------------------------------------------------
# Interface
# ---------------------------------------------------------------

def print_help():
    """Prints help"""
    print(
"""Usage:
imgres [options] <pattern> <greater-dim-limit>

Resizes all the images that match the given python regex pattern in the current directory  
to have the greater of the two dimensions at most as specified. 

Options:
-c, --confirm:           asks for confirmation before resizing images from each folder
-h, --help:              shows this help
-r, --recursive:         searches recursively also into subfolders
-l, --logs               makes a "./imgres-logs.txt" logfile from the run of the script
""")

def confirm(prompt=None, resp=False):
    """Prompts for yes or no response from the user. Returns True for yes and False for no.

    'resp' should be set to the default value assumed by the caller when user simply types ENTER.

    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n: 
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: 
    False
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True

    Taken from http://code.activestate.com/recipes/541096-prompt-the-user-for-confirmation/
    """
    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')
        
    while True:
        ans = input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print('please enter y or n.')
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False

def log(msg, f = None, end="\n"):
    """Logs given message by printing it and writing to given file"""
    print(msg, end=end)
    if f is not None:
        f.write(msg + end)

# ---------------------------------------------------------------
# Main
# ---------------------------------------------------------------

def main():
    # parse command line args and options
    argv = sys.argv[1:]
    print(argv)
    try:
        opts, args = getopt.getopt(argv, "hrcl", ["help", "recursive", "confirm", "logs"])
    except getopt.GetoptError:
        print_help()
        sys.exit()
       
    log_file = None
    confirmation = False
    recursively = False
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print_help()
            sys.exit()
        elif opt in ("-r", "--recursive"):
            recursively = True
        elif opt in ("-c", "--confirm"):
            confirmation = True
        elif opt in ("-l", "--logs"):
            log_file = open('imgres-logs.txt', 'w')
        else:
            print_help()
            sys.exit()

    if len(args) < 2:
        print("Must provide pattern and bigger-dim arguments")
        print_help()
        sys.exit()
    pattern = args[0]
    big_dim_limit = int(args[1])

    # build the list of matching files 
    log("Building list of files...", log_file)
    folder2files = {}
    if not recursively:
        folder2files['.'] = []
        for f in os.listdir("."):
            if re.search(pattern, f, re.IGNORECASE) is None:
                continue
            if not os.path.isfile(f):
                continue
            folder2files['.'].append(f)
    else:
        for root, dirs, files in os.walk(".", topdown=False):
            if root not in folder2files:
                folder2files[root] = []
            for f in files: 
                f_path = os.path.join(root, f)
                if re.search(pattern, f_path, re.IGNORECASE) is None:
                    continue
                if not os.path.isfile(f_path):
                    continue
                folder2files[root].append(f_path)

    # now go per-folder
    exception_count = 0
    for folder in folder2files:
        log("", log_file)
        log("*"*150, log_file)
        log("Processing folder: " + folder, log_file)
        folder_list = folder2files[folder]
        if (len(folder_list) == 0):
            log("No matching files...", log_file)
            continue

        # list the files and find out their dimensions
        log("Going to resize following images to have the greater of dimensions <= " 
            + str(big_dim_limit), log_file)
        sizes = []
        for f in folder_list:
            log("\t" + str(len(sizes) + 1) + ".) " + f, log_file, end=": ")
            cmd = 'convert "' + f + '" -print "%wx%h" /dev/null'
            out = subprocess.check_output(cmd, shell=True).decode("utf-8")
            w = int(out.split("x")[0])
            h = int(out.split("x")[1])
            sizes.append((w, h))
            log(str(w) + " x " + str(h), log_file)

        # confirmation check
        if confirmation:
            if not confirm("Do you really want to resize listed images?", True):
                sys.exit()

        # resize
        for i in range(len(folder_list)):
            max_dim = max(sizes[i][0], sizes[i][1])
            f = folder_list[i]
            order_str = "\t" + str(i + 1) + "/" + str(len(folder_list)) + ".) "
            try:
                if max_dim > big_dim_limit:
                    log(order_str + "resizing " + f, log_file)
                    if sizes[i][0] > sizes[i][1]:
                        subprocess.call('convert -resize "' + str(big_dim_limit) + '"X "' + f 
                            + '" "' + f + '"', shell=True)
                    else:
                        subprocess.call('convert -resize X"' + str(big_dim_limit) + '" "' + f 
                            + '" "' + f + '"', shell=True)
                else:
                    log(order_str + "no need to resize " + f, log_file)
            except Exception as e:
                exception_count += 1
                log(order_str + "exception " + str(e) + " for file " + f, log_file)

    log("All done. " + str(exception_count) + " exceptions")
    if log_file is not None:
        log_file.close()

if __name__ == '__main__':
    main()
