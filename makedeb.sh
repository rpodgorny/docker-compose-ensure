#!/bin/sh
set -e -x
exec python3 setup.py --command-packages=stdeb.command bdist_deb
