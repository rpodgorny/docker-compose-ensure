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


def main():
    args = docopt.docopt(__doc__)
    logging.basicConfig(level='DEBUG')
    dirname = args['<dirname>']
    pure_command = args['<command>']
    # FIXME: fun task - rewrite the following using ternary operator ;-)
    if '--' in pure_command:
        pure_command.pop(0)
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
            d.update(items_creation)  # FIXME: is this indented correctly?
        list(filter(lambda x: d.pop(x) if x in list(d.keys()) and x not in check_dirs else None, list(d.keys())))  # FIXME: this is abusing of functional constructs - either go fully functional (reduce?) or rewrite to plain old simple for loop ;-)

        t = time.time()
        for k, v in d.items():
            if t - v['interval'] > v['t_last']:
                logging.info('Will execute: %s', command)
                process = subprocess.run(command, shell=shell_, cwd=k)
                v['interval'] = min(v['interval'] * 2, 800) if process.returncode != 0 else check_delay  # FIXME: make 800 a global constant
                v['t_last'] = t
                logging.info('Return code: %s', process.returncode)
            else:
                logging.info('Not running, waiting for delay.')  # FIXME: remove this - it generates too much noise
        time.sleep(10)  # FIXME: make this a global constant
    return 0


if __name__ == "__main__":
    sys.exit(main())
