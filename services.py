#!/usr/bin/python3

'''
atxupdater.

Usage:
  services.py <dirname>

Arguments:
  <dirname>  Name of the directory with services.
'''


import docopt
import sys
import time
import subprocess
import logging
import os


def init_commands(dirname):
    # return list(map(lambda x: f'cd {dirname} && ./service{x}/run', services))
    symlinks = os.listdir(path=f'./{dirname}')
    ret = []
    for symlink in symlinks:
        fn = os.listdir(path=f'./{dirname}/{symlink}')
        command = f'./{fn[0]}'
        d = {
            'path': f'./{dirname}/{symlink}',
            'run_filename': command
        }
        ret.append(d)
    return ret


def show_outputs(command, returncode, stdout):
    logging.info('Command executed: %s' % command)
    logging.info('Return code: %s' % returncode)
    logging.info('Output: %s' % stdout)
    logging.info('------------------')
    return 0


def run_services(commands):
    for command in commands:
        process = subprocess.run(command['run_filename'], capture_output=True, shell=True, cwd=command['path'])
        show_outputs(process, process.returncode, process.stdout.decode())
        if process.returncode != 0:
            logging.info('Failed to execute: %s' % command)
            logging.info('Return code: %s' % process.returncode)
            return 1
    # failed_services = list(filter(lambda z: z != 0, map(lambda y: show_outputs(y, y.returncode, y.stdout.decode()), map(lambda x: subprocess.run(x, capture_output=True, shell=True), commands))))
    # if failed_services:
    #     logging.info('%s failed.' % failed_services[0])


def main():
    args = docopt.docopt(__doc__)
    logging.basicConfig(level='DEBUG', filename='services.log')
    logging.getLogger().addHandler(logging.StreamHandler()) # print logging messages to console
    dirname = args['<dirname>']
    commands = init_commands(dirname)
    while 1:
        error_check = run_services(commands)
        if error_check:
            logging.info('Service is down. Exiting.')
            break
        time.sleep(10)


if __name__ == "__main__":
    sys.exit(main())
