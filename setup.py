#!/usr/bin/python

from setuptools import setup

setup(
    name='dockerservices',
    version='2.2.2',
    description='Start docker services',
    long_description='Start docker services.',
    packages=['dockerservices'],
    install_requires=['docopt'],
    package_dir={'':'src'},
    entry_points={"console_scripts": ["dockerservices = dockerservices.dockerservices:main"]},
)
