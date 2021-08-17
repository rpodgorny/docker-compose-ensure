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


def init_commands(dirname, services):
    ret = []
    for service in services:
        command = f'cd {dirname} && ./service{service}/run'
        ret.append(command)
    return ret


def show_outputs(command, returncode, stdout):
    print('Command executed: ', command)
    print('Return code: ', returncode)
    print('Output: ', stdout)
    print('------------------')


def run_services(commands):
    for command in commands:
        process = subprocess.run(command, capture_output=True, shell=True)
        show_outputs(command, process.returncode, process.stdout.decode())
        if process.returncode != 0:
            print('Failed to execute: ', command, '\n return code: ', process.returncode)
            return 1


def main():
    args = docopt.docopt(__doc__)
    dirname = args['<dirname>']
    services = [1, 2, 3]
    commands = init_commands(dirname, services)

    while 1:
        error_check = run_services(commands)
        if error_check:
            print('Service is down. Exiting.')
            break
        time.sleep(10)


if __name__ == "__main__":
    sys.exit(main())
