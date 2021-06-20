from setuptools import find_packages, setup

from ffs import __version__ as version

exclude_packages = [
    "tests",
    "tests.*",
]

setup(name="ffs", version=version, packages=find_packages(exclude=exclude_packages))
