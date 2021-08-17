#!/usr/bin/python3

'''
Docker Services

Usage:
  services.py <dirname> <command>...

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


def init_directories(dirname):
    symlinks = os.listdir(path=f'./{dirname}')
    ret = []
    for symlink in symlinks:
        dir = f'./{dirname}/{symlink}'
        ret.append(dir)
    return ret


def show_outputs(process):
    logging.info('Process info: %s' % process)
    logging.info('Return code: %s' % process.returncode)
    logging.info('Output: %s' % process.stdout.decode())
    logging.info('------------------')
    return 0


def run_services(dirs, command):
    for dir in dirs:
        process = subprocess.run(command, capture_output=True, shell=True, cwd=dir)
        show_outputs(process)
        if process.returncode != 0:
            logging.info('Failed to execute: %s' % command['run_filename'])
            logging.info('Return code: %s' % process.returncode)
            return 1


def main():
    args = docopt.docopt(__doc__)
    logging.basicConfig(level='DEBUG', filename='services.log')
    logging.getLogger().addHandler(logging.StreamHandler()) # print logging messages to console
    dirname = args['<dirname>']
    command = args['<command>']
    dirs = init_directories(dirname)
    while 1:
        error_check = run_services(dirs, command[0])
        if error_check:
            logging.info('Service is down. Exiting.')
            break
        time.sleep(10)


if __name__ == "__main__":
    sys.exit(main())
