#! /usr/bin/env python
# 'backup-files.py' written by Tristan Maxson (tgmaxson@gmail.com)
import argparse
import os

parser = argparse.ArgumentParser(
    description='Backup files to a generated directory')
parser.add_argument(
    'filenames',
    type=str,
    nargs='+',
    help='Files to back up')
parser.add_argument(
    '--prefix',
    '-p',
    type=str,
    default="Backup-",
    help='Prefix for directory')
parser.add_argument(
    '--suffix',
    '-s',
    type=str,
    default="",
    help='Suffix for directory')
parser.add_argument(
    '--padding',
    '-P',
    type=int,
    default=5,
    help='Number of digits in directory name')
parser.add_argument(
    '--start',
    '-S',
    type=int,
    default=1,
    help='The number to start with in the directory name')
parser.add_argument(
    '--manual',
    '-m',
    action="store_const",
    const=True,
    default=False,
    help='Turn off automatic string splitting in filename')
parser.add_argument(
    '--silent',
    '-x',
    action="store_const",
    const=True,
    default=False,
    help='Turns off the printing of the directory name')
parser.add_argument(
    '--action',
    '-a',
    type=str,
    default="cp",
    help='Defines the action to call to move the file to the directory, \
          will be run as "$action $filename $newdirectory"')


def gen_dir(number):
    '''
    Generates a directory name based on the parameters given and the current
    number that needs to be evaluated.
    '''
    return '{0}{1}{2}'.format(args.prefix,
                              str(number).zfill(args.padding),
                              args.suffix)


def mkdir(dir):
    '''
    Makes a directory and returns true if possible,
    else return false if exists.
    '''
    try:
        os.mkdir(dir)
        return True
    except OSError as e:
        if e.errno == 17:
            return False
        else:
            raise

# Parse args and manipulate filenames
args = parser.parse_args()
if not args.manual:
    args.filenames = filter(None, " ".join(args.filenames).split(" "))

# Make the directory
dirname = ""
for dir in range(args.start, (10**args.padding)):
    dirname = gen_dir(dir)
    if mkdir(dirname):
        break
else:
    raise RuntimeError('Ran out of available backup directories.')

# Take actions on each file
for filename in args.filenames:
    os.system("{0} {1} {2} 2>/dev/null || :".format(args.action,
                                   filename,
                                   dirname))

# Report directory name
if not args.silent:
    print dirname

