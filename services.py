#!/usr/bin/python3

'''
Docker Services

Usage:
  services.py <dirname> <command>

Arguments:
  <dirname>  Name of the directory with services.
  <command>  Command that will be executed.
'''


import docopt
import sys
import time
import subprocess
import logging
import os


def run_services(dirs, command):
    for dir in dirs:
        process = subprocess.run(command, capture_output=True, shell=True, cwd=dir)
        logging.info('Command executed: ', command)
        logging.info('Return code: ', process.returncode)


def main():
    args = docopt.docopt(__doc__)
    logging.basicConfig(level='DEBUG')
    logging.getLogger().addHandler(logging.StreamHandler()) # print logging messages to console
    dirname = args['<dirname>']
    command = args['<command>']
    dirs = [f'./{dirname}/{x}' for x in [x for x in os.listdir(dirname) if os.path.islink('./' + dirname + '/' + x)]]
    while 1:
        run_services(dirs, command)
        time.sleep(10)


if __name__ == "__main__":
    sys.exit(main())
