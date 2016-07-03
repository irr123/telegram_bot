# coding: utf-8
import os
from setuptools import setup, find_packages

long_description = open('README.TXT').read()

setup(
    name='JustAnotherBot',
    version='0.0.1',
    packages=find_packages(),
    license='MIT',
    url='https://github.com/cirno-baka/telegram_bot',
    author='Cirno',
    install_requires=open('requirements.txt').read(),
    include_package_data=True,
    long_description=long_description,
)