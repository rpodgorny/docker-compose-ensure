#!/usr/bin/python3

'''
Docker Services

Usage:
  services.py [options] <dirname> <command>...

Arguments:
  <dirname>  Name of the directory with services.
  <command>  Command that will be executed.

Options:
  --check-delay <check-delay>  Specify interval how often process will be checked (secs).
  --shell                      Set shell arg to True.
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
    if '--' in pure_command:
        pure_command.pop(0)
    shell_ = args['--shell']
    command = ' '.join(pure_command) if shell_ else pure_command
    check_delay = float(args['--check-delay'])
    dirs = [f'./{dirname}/{x}' for x in os.listdir(dirname) if os.path.islink(f'./{dirname}/{x}')]
    times = [[int(check_delay), 0] for x in range(len(dirs))]
    d = dict(zip(dirs, times))
    while 1:
        check_dirs = [f'./{dirname}/{x}' for x in os.listdir(dirname) if os.path.islink(f'./{dirname}/{x}')]
        for i in check_dirs:
            if i not in d:
                d[i] = [check_delay, 0]
        list(filter(lambda x: d.pop(x) if x in list(d.keys()) and x not in check_dirs else None, list(d.keys())))
        t = time.time()
        for k, v in d.items():
            if t - v[0] > v[1]:
                logging.info('Command executed: %s', command)
                process = subprocess.run(command, capture_output=True, shell=shell_, cwd=k)
                v[0] = min(v[0] * 2, 800) if process.returncode != 0 else check_delay
                v[1] = t
                logging.info('Return code: %s', process.returncode)
            else:
                logging.info('Not running, waiting for delay.')
        time.sleep(10)
    return 0


if __name__ == "__main__":
    sys.exit(main())
