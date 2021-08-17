#!/usr/bin/python3

'''
atxupdater.

Usage:
  ensure.py <dirname>

Arguments:
  <dirname>  Name of the directory with services.
'''


import docopt
import sys
import time
import subprocess
import logging


def init_commands(dirname, services):
    return list(map(lambda x: f'cd {dirname} && ./service{x}/run', services))


def show_outputs(command, returncode, stdout):
    logging.info('Command executed: %s' % command)
    logging.info('Return code: %s' % returncode)
    logging.info('Output: %s' % stdout)
    logging.info('------------------')
    return 0


def run_services(commands):
    for command in commands:
        process = subprocess.run(command, capture_output=True, shell=True)
        show_outputs(command, process.returncode, process.stdout.decode())
        if process.returncode != 0:
            logging.info('Failed to execute: %s' % command)
            logging.info('Return code: %s' % process.returncode)
            return 1


def main():
    args = docopt.docopt(__doc__)
    logging.basicConfig(level='DEBUG', filename='services.log')
    logging.getLogger().addHandler(logging.StreamHandler()) # print logging messages to console
    dirname = args['<dirname>']
    services = [1, 2, 3]
    commands = init_commands(dirname, services)

    while 1:
        error_check = run_services(commands)
        if error_check:
            logging.info('Service is down. Exiting.')
            break
        time.sleep(10)


if __name__ == "__main__":
    sys.exit(main())
