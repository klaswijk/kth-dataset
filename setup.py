import os
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="kth_dataset",
    version="1.0",
    author="Klas Wijk",
    license="MIT",
    packages=find_packages(),
    install_requires=required
)