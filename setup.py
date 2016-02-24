# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from setuptools import setup, find_packages

setup(name='illiad',
    version='0.8',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
)
