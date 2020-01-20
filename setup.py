# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='automated-speedtest',
    version='0.1.0',
    description='Keep your internet provider honest with speed tests',
    long_description=readme,
    author='Geoff Wellington',
    author_email='nit3owldev@gmail.com',
    url='https://github.com/nit3owl/automated-speedtest',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
