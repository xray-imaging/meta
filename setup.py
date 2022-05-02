from setuptools import setup, find_packages
from setuptools.command.install import install
import os


setup(
    name='meta',
    version=open('VERSION').read().strip(),
    author='Francesco De Carlo',
    author_email='decarlof@gmail.com',
    url='https://github.com/xray-imaging/meta',
    packages=find_packages(),
    include_package_data = True,
    description='library to extract meta data from a file, supported format: hdf, ...',
    zip_safe=False,
)