# -*- coding: utf-8
"""
Contains unit tests for :mod:`mr_freeze.ui.ui_loader
"""
import unittest
from PyQt4 import QtGui
from mr_freeze.ui.ui_loader import Main
import sys


class TestUIDefaultState(unittest.TestCase):
    """
    Tests that the UI loads correctly
    """
    def setUp(self):
        self.app = QtGui.QApplication(sys.argv)
        self.ui = Main()

    def test_default_state(self):
        self.assertEqual(
            0,
            self.ui.ui.lcdNumber_4.value()
        )
