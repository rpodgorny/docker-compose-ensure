#!/usr/bin/python3

'''
Docker Services

Usage:
  services.py <dirname> <command> [options]

Arguments:
  <dirname>  Name of the directory with services.
  <command>  Command that will be executed.

Options:
  --sleep <sleep>  Specify how often data will be send (secs).
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
        logging.info('Command executed: %s', command)
        logging.info('Return code: %s', process.returncode)


def main():
    args = docopt.docopt(__doc__)
    logging.basicConfig(level='DEBUG')
    dirname = args['<dirname>']
    command = args['<command>']
    sleep_time = args['--sleep']
    sleep_time = float(sleep_time) if sleep_time else 5
    dirs = [f'./{dirname}/{x}' for x in [x for x in os.listdir(dirname) if os.path.islink('./' + dirname + '/' + x)]]
    while 1:
        run_services(dirs, command)
        time.sleep(sleep_time)


if __name__ == "__main__":
    sys.exit(main())
