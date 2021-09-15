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
    # FIXME: fun task - rewrite the following using ternary operator ;-) -> nice try but incorrect - list.pop() returns the popped item, not a new list with one item popped
    pure_command = pure_command if not '--' in pure_command else [x for x in pure_command if x != '--']  # not a big fan... but can not find out any other functional way
    shell_ = args['--shell']
    command = ' '.join(pure_command) if shell_ else pure_command
    check_delay = float(args['--check-delay'])
    d = {}
    while 1:
        check_dirs = [f'./{dirname}/{x}' for x in os.listdir(dirname) if os.path.islink(f'./{dirname}/{x}')]
        for i in check_dirs:
            if i not in d:
                items_creation = {i: {
                    'interval': check_delay,
                    't_last': 0,
                }}
                d.update(items_creation)  # FIXME: items_creation may be undefined if the condition above is false
		# FIXME: better -> now try to rewrite it to dict comprehension
        for key in list(d.keys()):
            if key in d.keys() and key not in check_dirs:
                d.pop(key)
        # d_comp = {d.pop(n) for n in d.keys() if n not in check_dirs}

        t = time.time()
        for k, v in d.items():
            if t - v['interval'] > v['t_last']:
                logging.info('Will execute: %s', command)
                process = subprocess.run(command, shell=shell_, cwd=k)
                v['interval'] = min(v['interval'] * 2, INTERVAL_LIMIT) if process.returncode != 0 else check_delay
                v['t_last'] = t
                logging.info('Return code: %s', process.returncode)
            # FIXME: remove this - it generates too much noise
        time.sleep(TIME_SLEEP)
    return 0


if __name__ == "__main__":
    sys.exit(main())
