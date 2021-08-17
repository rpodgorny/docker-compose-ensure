#!/bin/bash
set -e -x
exec pipenv run python services.py "$@"
