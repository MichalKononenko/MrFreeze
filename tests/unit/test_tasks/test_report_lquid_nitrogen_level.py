"""
Contains unit tests for :mod:`mr_freeze.tasks.report_liquid_nitrogen_level`
"""
import unittest
import unittest.mock as mock
from concurrent.futures import Executor
from mr_freeze.devices.cryomagnetics_lm510_adapter import CryomagneticsLM510
from mr_freeze.tasks.report_liquid_nitrogen_level import ReportLiquidNitrogenLevel


class TestReportLiquidNitrogenLevel(unittest.TestCase):
    gauge = mock.MagicMock(spec=CryomagneticsLM510)  # type: CryomagneticsLM510
    ln2_channel = 2
    executor = mock.MagicMock(spec=Executor)

    def setUp(self):
        self.task = ReportLiquidNitrogenLevel(
            self.gauge, ln2_channel=self.ln2_channel
        )


class TestInitializer(TestReportLiquidNitrogenLevel):
    def test_initializer(self):
        self.assertEqual(self.gauge, self.task.gauge)
        self.assertEqual(self.ln2_channel, self.task.ln_2_channel)


class TestCall(TestReportLiquidNitrogenLevel):
    def test_call(self):
        self.task(self.executor)
        self.assertTrue(
            self.executor.submit.called
        )
        self.assertTrue(hasattr(self._task_function, '__call__'))

    def test_run_task(self):
        self.task(self.executor)
        ln2_level = self._task_function()
        self.assertEqual(
            self.gauge.level_meter.channel_2_measurement, ln2_level
        )

    @property
    def _task_function(self):
        return self.executor.submit.call_args[0][0]