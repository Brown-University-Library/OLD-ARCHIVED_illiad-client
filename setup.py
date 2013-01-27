#import ez_setup
#ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(name='illiad',
    version='0.2',
    packages=find_packages(),
    package_data={'illiad': ['test/data/*.*']},
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
)