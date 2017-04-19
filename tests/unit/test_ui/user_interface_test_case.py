# coding=utf-8
"""
Contains a base class for testing the user interface. This class is
responsible for creating and then tearing down the UI

.. warning::

    Python 3 and PyQt4 do not get along nicely. In fact, Python does some
    funky things when garbage collecting the assets used by a PyQt4
    application. The result of this is that when one attempts to restart a
    Qt application in the same process (as you're wont to do in a test
    suite), the test suite will SEGFAULT.

    Therefore, any test of the user interface should take care to inherit
    from this class
"""
import unittest
from PyQt4 import QtGui
from concurrent.futures import ThreadPoolExecutor
from mr_freeze.ui.ui_loader import Main
from mr_freeze.resources.application_state import Store
import sys


class UserInterfaceTestCase(unittest.TestCase):
    number_of_ui_threads = 20

    @classmethod
    def setUpClass(cls):
        cls.executor = ThreadPoolExecutor(cls.number_of_ui_threads)
        cls.store = Store(cls.executor)
        cls.app = QtGui.QApplication(sys.argv)
        cls.app.deleteLater()
        cls.ui = Main(cls.store)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'app'):
            cls.app.quit()
