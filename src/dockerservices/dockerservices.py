#!/usr/bin/python3

'''
Docker Services

Usage:
  services.py [options] <dirname> <command>...

Arguments:
  <dirname>  Name of the directory with services.
  <command>  Command that will be executed.

Options:
  --check-delay=<n>  Specify interval how often process will be checked (secs).
  --shell            Set shell arg to True.
'''


import docopt
import sys
import time
import subprocess
import logging
import os

TIME_SLEEP = 10
INTERVAL_LIMIT = 800


def main():
    args = docopt.docopt(__doc__)
    logging.basicConfig(level='DEBUG')
    dirname = args['<dirname>']
    pure_command = args['<command>']
    pure_command = pure_command if pure_command[0] != '--' else pure_command[1:]
    shell_ = args['--shell']
    command = ' '.join(pure_command) if shell_ else pure_command
    check_delay = float(args['--check-delay'])
    d = {}
    while 1:
        check_dirs = [f'./{dirname}/{x}' for x in os.listdir(dirname) if os.path.islink(f'./{dirname}/{x}')]
        for i in check_dirs:
            if i not in d:
				# FIXME: get rid of "items_creation" -> just use d.update with the following dict
                items_creation = {i: {
                    'interval': check_delay,
                    't_last': 0,
                }}
                d.update(items_creation)
        d = {k: v for (k, v) in d.items() if k in check_dirs}
        t = time.time()
        for k, v in d.items():
            if t - v['interval'] > v['t_last']:
                logging.info('Will execute: %s', command)
                process = subprocess.run(command, shell=shell_, cwd=k)
				# FIXME: update the dict at once -> use "update", not two separate value assignments
                v['interval'] = min(v['interval'] * 2, INTERVAL_LIMIT) if process.returncode != 0 else check_delay
                v['t_last'] = t
                logging.info('Return code: %s', process.returncode)
        time.sleep(TIME_SLEEP)
    return 0


if __name__ == "__main__":
    sys.exit(main())
