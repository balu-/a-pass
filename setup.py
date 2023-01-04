# -*- coding: utf-8 -*-

# Learn more: url

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='apass',
    version='0.3.0',
    description='password manager based an age',
    long_description=readme,
    author='Arwed Coutandin',
    author_email='me@a-pass.de',
    url='https://www.a-pass.de',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)