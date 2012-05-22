import unittest
from test import account
from test import parsers

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(account.suite())
    test_suite.addTest(parsers.suite())
    return test_suite

runner = unittest.TextTestRunner()
runner.run(suite())