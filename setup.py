# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='fusefit',
    version='1',
    description='Combine two TCX files, adding Heart Rate',
    long_description=readme,
    author='David Bradway',
    author_email='david.bradway@gmail.com',
    url='https://github.com/davidbradway/fusefit',
    license=license,
    packages=find_packages(exclude=('tests', 'docs', 'flask', 'tmp'))
)

