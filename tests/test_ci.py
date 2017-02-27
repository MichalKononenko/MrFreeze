"""
Contains unit tests for :meth:`ci_test`
"""
import unittest
from mr_freeze.ci_test import add_one


class TestContinuousIntegration(unittest.TestCase):
    """
    Test that the CI method works
    """
    numberToAdd = 1
    expectedAnswer = 2

    def test_add_one(self):
        self.assertEqual(self.expectedAnswer, add_one(self.numberToAdd))
