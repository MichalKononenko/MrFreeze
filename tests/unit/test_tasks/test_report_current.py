# -*- coding: utf-8 -*-
"""
Contains unit tests for the task that reports the current
"""
import unittest
import unittest.mock as mock
from numpy import nan
from quantities import A
from concurrent.futures import Executor
from numpy.testing import assert_array_equal
from mr_freeze.devices.cryomagnetics_4g_adapter import Cryomagnetics4G
from mr_freeze.exceptions import NoEchoedCommandFoundError
from mr_freeze.tasks.report_current import ReportCurrent
from mr_freeze.resources.abstract_store import Store
from mr_freeze.resources.application_state import Current


class TestReportCurrent(unittest.TestCase):
    """
    Base class for the test
    """
    def setUp(self):
        self.gauge = mock.MagicMock(
            spec=Cryomagnetics4G)  # type: Cryomagnetics4G
        self.executor = mock.MagicMock(spec=Executor)  # type: Executor
        self.store = mock.MagicMock(spec=Store)  # type: Store
        self.task = ReportCurrent(gauge=self.gauge, store=self.store)


class TestVariableType(TestReportCurrent):
    def test_type(self):
        self.assertEqual(
            Current,
            self.task.variable_type
        )


class TestVariable(TestReportCurrent):
    def test_report_no_error(self):
        assert_array_equal(
            self.gauge.current,
            self.task.variable
        )

    def test_error(self):
        type(self.gauge).current = mock.PropertyMock(
            side_effect=NoEchoedCommandFoundError("Kaboom")
        )
        assert_array_equal(
            nan * A,
            self.task.variable
        )