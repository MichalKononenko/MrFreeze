# coding=utf-8
"""
Contains unit tests for the task that sets the lower sweep current
"""
import unittest
import unittest.mock as mock
from mr_freeze.devices.cryomagnetics_4g_adapter import Cryomagnetics4G
from mr_freeze.tasks.set_lower_sweep_current import SetLowerSweepCurrent
from quantities import Quantity, amperes
from concurrent.futures import Executor


class TestSetLowerCurrent(unittest.TestCase):
    def setUp(self):
        self.sweep_current = 10.0 * amperes  # type: Quantity
        self.power_supply = mock.MagicMock(spec=Cryomagnetics4G)
        self.executor = mock.MagicMock(spec=Executor)  # type: Executor
        self.task = SetLowerSweepCurrent(self.sweep_current, self.power_supply)


class TestTask(TestSetLowerCurrent):
    def test_task(self):
        self.task.task(self.executor)
        self.assertEqual(
            self.sweep_current,
            self.power_supply.lower_sweep_current
        )
