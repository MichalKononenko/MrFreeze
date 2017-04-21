# coding=utf-8
"""
Tests that the upper sweep current is set correctly
"""
import unittest
import unittest.mock as mock
from mr_freeze.devices.cryomagnetics_4g_adapter import Cryomagnetics4G
from mr_freeze.tasks.set_upper_sweep_current import SetUpperSweepCurrent
from quantities import Quantity, amperes
from concurrent.futures import Executor


class TestSetUpperCurrent(unittest.TestCase):
    def setUp(self):
        self.sweep_current = 10.0 * amperes  # type: Quantity
        self.power_supply = mock.MagicMock(spec=Cryomagnetics4G)
        self.executor = mock.MagicMock(spec=Executor)
        self.task = SetUpperSweepCurrent(self.sweep_current, self.power_supply)


class TestTask(TestSetUpperCurrent):
    def test_task(self):
        self.task.task(self.executor)
        self.assertEqual(
            self.sweep_current,
            self.power_supply.upper_sweep_current
        )
