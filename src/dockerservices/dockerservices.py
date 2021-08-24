#!/usr/bin/python3

'''
Docker Services

Usage:
  services.py [options] <dirname> <command>...

Arguments:
  <dirname>  Name of the directory with services.
  <command>  Command that will be executed.

Options:
  --sleep <sleep>  Specify how often data will be send (secs).
  --shell          Set shell arg to True.
'''


import docopt
import sys
import time
import subprocess
import logging
import os


def run_services(dirs, command, shell_):
    for dir_ in dirs:
        logging.info('Command executed: %s', command)
        process = subprocess.run(command, capture_output=True, shell=shell_, cwd=dir_)
        logging.info('Return code: %s', process.returncode)


def main():
    args = docopt.docopt(__doc__)
    logging.basicConfig(level='DEBUG')
    dirname = args['<dirname>']
    pure_command = args['<command>']
    if '--' in pure_command:
        pure_command.pop(0)
    shell = args['--shell']
    shell = True if shell else False
    command = ' '.join(pure_command)
    sleep_time = args['--sleep']
    sleep_time = float(sleep_time) if sleep_time else 5
    dirs = [f'./{dirname}/{x}' for x in os.listdir(dirname) if os.path.islink(f'./{dirname}/{x}')]
    while 1:
        run_services(dirs, command, shell)
        time.sleep(sleep_time)


if __name__ == "__main__":
    sys.exit(main())
