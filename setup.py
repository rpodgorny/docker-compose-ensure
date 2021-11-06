#!/usr/bin/python3

from setuptools import setup
from dockercomposeensure.version import __version__

setup(
    name="docker-compose-ensure",
    version=__version__,
    description="Make sure my docker-compose services are running",
    long_description="Make sure my docker-compose services are running",
    packages=["dockercomposeensure"],
    install_requires=["docopt"],
    package_dir={"": "src"},
    entry_points={"console_scripts": ["docker-compose-ensure = dockercomposeensure.dockercomposeensure:main"]},
    include_package_data=True,
    data_files=[("/usr/lib/systemd/system/", ["docker-compose-ensure.service"])],
    package_data={"": ["docker-compose-ensure.service"]},
)
