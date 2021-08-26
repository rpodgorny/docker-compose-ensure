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


def main():
    args = docopt.docopt(__doc__)
    logging.basicConfig(level='DEBUG')
    dirname = args['<dirname>']
    pure_command = args['<command>']
    if '--' in pure_command:
        pure_command.pop(0)
    shell_ = args['--shell']
    command = ' '.join(pure_command) if shell_ else pure_command
    sleep_time = args['--sleep']
    sleep_time = float(sleep_time) if sleep_time else 5
    dirs = [f'./{dirname}/{x}' for x in os.listdir(dirname) if os.path.islink(f'./{dirname}/{x}')]
    times = []
    for i in range(len(dirs)):
          times.append(sleep_time)
    while 1:
        for dir_ in dirs:
          index = dirs.index(dir_)
          time_index = times[index]
          logging.info('Command executed: %s', command)
          process = subprocess.run(command, capture_output=True, shell=shell_, cwd=dir_)
          if process.returncode != 0:
            time_index += time_index
          times[index] = time_index
          logging.info('Return code: %s', process.returncode)
          time.sleep(time_index)


if __name__ == "__main__":
    sys.exit(main())
