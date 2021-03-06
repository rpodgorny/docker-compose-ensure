#!/usr/bin/python3

"""
docker-compose-ensure

Usage:
  docker-compose-ensure [options] <dirname> <command>...

Arguments:
  <dirname>  Name of the directory with symlinks to services.
  <command>  Command that will be executed.

Options:
  --interval=<n>  How often process will be checked (secs).
  --shell         Set shell arg to True for subprocess.
"""


from .version import __version__
import docopt
import sys
import time
import subprocess
import logging
import os


SLEEP = 10
INTERVAL_LIMIT = 600


def main():
    args = docopt.docopt(__doc__, version=__version__)
    log_level = "INFO"
    logging.basicConfig(level=log_level)
    logging.info("starting docker-compose-ensure v%s" % __version__)
    dirname = args["<dirname>"]
    pure_command = args["<command>"]
    pure_command = pure_command if pure_command[0] != "--" else pure_command[1:]
    shell_ = args["--shell"]
    command = " ".join(pure_command) if shell_ else pure_command
    interval = float(args["--interval"]) if args["--interval"] else 60
    d = {}
    while 1:
        check_dirs = [x for x in os.listdir(dirname) if os.path.islink(f"{dirname}/{x}")]
        logging.debug("found dirs: %s" % check_dirs)
        for i in check_dirs:
            if i not in d:
                d[i] = {
                    "interval": interval,
                    "t_last": 0,
                }
        d = {k: v for (k, v) in d.items() if k in check_dirs}
        t = time.time()
        for k, v in d.items():
            if t - v["interval"] > v["t_last"]:
                logging.info("%s -> %s" % (k, command))
                p = subprocess.run(command, shell=shell_, cwd=f"{dirname}/{k}")
                d[k] = {
                    "interval": min(v["interval"] * 2, INTERVAL_LIMIT) if p.returncode != 0 else interval,
                    "t_last": t,
                }
                logging.info("%s: res=%s" % (k, p.returncode))
        logging.debug("sleep %s" % SLEEP)
        time.sleep(SLEEP)
    return 0


if __name__ == "__main__":
    sys.exit(main())
