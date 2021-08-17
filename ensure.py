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


def cd_up():
    return subprocess.run('cd ..', shell=True)


def gen_command(dirname, service_number):
    pass  # TODO


def run_services(dirname):
    command = f'cd {dirname}'
    subprocess.run(command, capture_output=True, shell=True)
    first = subprocess.run('cd active && ./service1/run', capture_output=True, shell=True)
    print('first:: ', first)
    print('first ret:: ', first.returncode)
    print('first stdout:: ', first.stdout.decode())
    second = subprocess.run('cd active && ./service2/run', capture_output=True, shell=True) # TODO make a loop (map?)
    print('sec:: ', second)
    print('sec ret:: ', second.returncode)
    print('sec stdout:: ', second.stdout.decode())
    third = subprocess.run('cd active && ./service3/run', capture_output=True, shell=True)
    print('sec:: ', third)
    print('sec ret:: ', third.returncode)
    print('sec stdout:: ', third.stdout.decode())
    print('done')
    if first.returncode + second.returncode + third.returncode != 0:  # TODO look which one failed and print it
        return 1


def main():
    args = docopt.docopt(__doc__)
    dirname = args['<dirname>']
    print(dirname)
    command = f'ls -l {dirname}'
    output = subprocess.run(command, capture_output=True, shell=True)
    return_code = output.returncode
    print('command: ', command)
    print(output)
    if not return_code:
        print('There is no return code. Everything went well.')

    while 1:
        error_check = run_services(dirname)
        if error_check:
            print('Something failed. Exiting.')
            break
        time.sleep(10)


if __name__ == "__main__":
    sys.exit(main())
