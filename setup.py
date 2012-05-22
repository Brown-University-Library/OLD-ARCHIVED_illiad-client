#import ez_setup
#ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(name='illiad',
    version='0.1',
    packages=find_packages(),
    package_data={'illiad': ['test/data/*.*']},
)