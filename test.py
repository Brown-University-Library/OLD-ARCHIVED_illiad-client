# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
from test import account
from test import parsers

import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(account.suite())
    test_suite.addTest(parsers.suite())
    return test_suite

runner = unittest.TextTestRunner()
runner.run(suite())
