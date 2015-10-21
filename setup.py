# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from setuptools import setup, find_packages

setup(name='illiad',
    version='0.3',
    packages=find_packages(),
    package_data={'illiad': ['test/data/*.*']},
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
)
