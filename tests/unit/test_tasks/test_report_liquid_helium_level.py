"""
Contains unit tests for :mod:`mr_freeze.tasks.report_liquid_helium_level`
"""
import unittest
import unittest.mock as mock
from concurrent.futures import Executor
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

        self.task = ReportLiquidHeliumLevel(self.gauge, self.lhe_channel)


class TestTask(TestReportLiquidHeliumLevel):

    def test_task_channel_1(self) -> None:
        self.task.lhe_channel = 1
        result = self.task.task(self.executor)

        self.assertEqual(self.gauge.channel_1_measurement, result)

    def test_task_channel_2(self) -> None:
        self.task.lhe_channel = 2
        result = self.task.task(self.executor)

        self.assertEqual(self.gauge.channel_2_measurement, result)

    def test_task_error(self) -> None:
        self.task.lhe_channel = 3

        with self.assertRaises(RuntimeError):
            self.task.task(self.executor)