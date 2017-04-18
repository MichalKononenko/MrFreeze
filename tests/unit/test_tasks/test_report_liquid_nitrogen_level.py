# -*- coding: utf-8 -*-
"""
Contains unit tests for :mod:`mr_freeze.tasks.report_liquid_nitrogen_level`
"""
import unittest
import unittest.mock as mock
from numpy import nan
from quantities import cm
from concurrent.futures import Executor
from numpy.testing import assert_array_equal
from mr_freeze.exceptions import NoEchoedCommandFoundError
from mr_freeze.resources.abstract_store import Store
from mr_freeze.resources.application_state import LiquidNitrogenLevel
from mr_freeze.devices.cryomagnetics_lm510_adapter import CryomagneticsLM510
from mr_freeze.tasks.report_liquid_nitrogen_level import \
    ReportLiquidNitrogenLevel


class TestReportLiquidNitrogenLevel(unittest.TestCase):
    """
    Base class for tests of the liquid nitrogen level
    """

    def setUp(self):
        """
        Create an instance of the task
        """
        self.gauge = mock.MagicMock(
            spec=CryomagneticsLM510)  # type: CryomagneticsLM510
        self.ln2_channel = 2
        self.executor = mock.MagicMock(spec=Executor)
        self.store = mock.MagicMock(spec=Store)  # type: Store

        self.task = ReportLiquidNitrogenLevel(
            self.gauge, self.store, ln2_channel=self.ln2_channel
        )


class TestInitializer(TestReportLiquidNitrogenLevel):
    """
    Contains unit tests for :meth:`__init__`
    """
    def test_initializer(self):
        """
        Assert that the instance was constructed correctly
        """
        self.assertEqual(self.gauge, self.task.gauge)
        self.assertEqual(self.ln2_channel, self.task.ln_2_channel)

    def test_variable_type(self):
        self.assertEqual(
            LiquidNitrogenLevel, self.task.variable_type
        )


class TestVariable(TestReportLiquidNitrogenLevel):
    """
    Contains unit tests for the variable level
    """
    def test_channel_1_variable(self):
        self.task.ln_2_channel = 1
        self.assertEqual(
            self.task.variable,
            self.gauge.channel_1_measurement
        )

    def test_channel_2_variable(self):
        self.task.ln_2_channel = 2
        self.assertEqual(
            self.task.variable,
            self.gauge.channel_2_measurement
        )

    def test_error(self):
        type(self.gauge).channel_1_measurement = mock.PropertyMock(
            side_effect=NoEchoedCommandFoundError(
                "Big explosion! Really the best explosion!"
            )
        )
        assert_array_equal(
            nan * cm,
            self.task.variable
        )
