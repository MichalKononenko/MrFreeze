# -*- coding: utf-8 -*-
"""
Contains unit tests for :mod:`mr_freeze.tasks.report_liquid_helium_level`
"""
import unittest
import unittest.mock as mock
from concurrent.futures import Executor
from mr_freeze.resources.abstract_store import Store
from mr_freeze.resources.application_state import LiquidHeliumLevel
from mr_freeze.devices.cryomagnetics_lm510_adapter import CryomagneticsLM510
from mr_freeze.tasks.report_liquid_helium_level import ReportLiquidHeliumLevel


class TestReportLiquidHeliumLevel(unittest.TestCase):
    """
    Base class for unit tests of
    :class:`mr_freeze.tasks.report_liquid_helium_level.ReportLiquidHeliumLevel`
    """
    def setUp(self) -> None:
        self.lhe_channel = 1
        self.gauge = mock.MagicMock(
            spec=CryomagneticsLM510)  # type: CryomagneticsLM510
        self.executor = mock.MagicMock(
            spec=Executor)  # type: Executor
        self.store = mock.MagicMock(
            spec=Store
        )  # type: Store

        self.task = ReportLiquidHeliumLevel(
            self.gauge, self.store, self.lhe_channel
        )


class TestVariableType(TestReportLiquidHeliumLevel):
    def test_variable_type(self):
        self.assertEqual(
            LiquidHeliumLevel,
            self.task.variable_type
        )


class TestTask(TestReportLiquidHeliumLevel):

    def test_task_channel_1(self) -> None:
        self.task.lhe_channel = 1
        self.assertEqual(self.gauge.channel_1_measurement, self.task.variable)

    def test_task_channel_2(self) -> None:
        self.task.lhe_channel = 2
        self.assertEqual(self.gauge.channel_2_measurement, self.task.variable)

    def test_task_error(self) -> None:
        self.task.lhe_channel = 3

        with self.assertRaises(RuntimeError):
            self.task.variable
