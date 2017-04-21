# -*- coding: utf-8 -*-
"""
Contains unit tests for :mod:`mr_freeze.tasks.report_magnetic_field`
"""
import unittest
import unittest.mock as mock
from concurrent.futures import Executor
from mr_freeze.devices.lakeshore_475 import Lakeshore475
from mr_freeze.resources.abstract_store import Store
from mr_freeze.tasks.report_magnetic_field import ReportMagneticField
from mr_freeze.exceptions import NoEchoedCommandFoundError
from numpy import nan
from numpy.testing import assert_array_equal
from quantities import gauss


class TestReportMagneticField(unittest.TestCase):
    """
    Base class for unit tests of
    :class:`mr_freeze.tasks.report_magnetic_field.ReportMagneticField`
    """
    def setUp(self):
        """
        Initialize the task fixture
        """
        self.gauge = mock.MagicMock(spec=Lakeshore475)  # type: Lakeshore475
        self.executor = mock.MagicMock(spec=Executor)  # type: Executor
        self.store = mock.MagicMock(spec=Store)  # type: Store
        self.task = ReportMagneticField(gauge=self.gauge, store=self.store)


class TestInitializer(TestReportMagneticField):
    """
    Contains unit tests for the initializer
    """
    def test_field(self):
        """
         Assert that the correct gauge was instantiated
        """
        self.assertEqual(self.gauge, self.task.gauge)
        self.assertEqual(self.store, self.task.store)


class TestVariable(TestReportMagneticField):
    """
    Contains unit tests for the variable reporter
    """
    def test_variable(self):
        self.assertEqual(
            self.gauge.field,
            self.task.variable
        )

    def test_variable_with_error(self):
        type(self.gauge).field = mock.PropertyMock(
            side_effect=NoEchoedCommandFoundError
        )
        assert_array_equal(
            nan * gauss,
            self.task.variable
        )
