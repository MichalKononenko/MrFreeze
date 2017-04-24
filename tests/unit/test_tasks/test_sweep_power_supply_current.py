# coding=utf-8
"""
Contains unit tests to test the power supply sweep
"""
import unittest
import unittest.mock as mock
from concurrent.futures import Executor
from mr_freeze.tasks.sweep_power_supply_current import SweepPowerSupply
from mr_freeze.devices.cryomagnetics_4g_adapter import Cryomagnetics4G


class TestSweepPowerSupply(unittest.TestCase):
    def setUp(self):
        self.direction = mock.MagicMock(spec=SweepPowerSupply.Direction)
        self.power_supply = mock.MagicMock(spec=Cryomagnetics4G)
        self.fast_sweep = mock.MagicMock(spec=bool)
        self.executor = mock.MagicMock(spec=Executor)


class TestTask(TestSweepPowerSupply):
    def test_up(self):
        direction = SweepPowerSupply.Direction.UP
        task = SweepPowerSupply(direction, self.power_supply, self.fast_sweep)
        task.task(self.executor)

        self.assertEqual(
            mock.call(fast=self.fast_sweep),
            self.power_supply.sweep_up.call_args
        )

    def test_down(self):
        direction = SweepPowerSupply.Direction.DOWN
        task = SweepPowerSupply(direction, self.power_supply, self.fast_sweep)
        task.task(self.executor)

        self.assertEqual(
            mock.call(fast=self.fast_sweep),
            self.power_supply.sweep_down.call_args
        )

    def test_zero(self):
        direction = SweepPowerSupply.Direction.ZERO
        task = SweepPowerSupply(direction, self.power_supply, self.fast_sweep)
        task.task(self.executor)

        self.assertEqual(
            mock.call(fast=self.fast_sweep),
            self.power_supply.sweep_zero.call_args
        )

    def test_pause(self):
        direction = SweepPowerSupply.Direction.PAUSE
        task = SweepPowerSupply(direction, self.power_supply, self.fast_sweep)
        task.task(self.executor)

        self.assertTrue(
            self.power_supply.pause_sweep.called
        )

    def test_error(self):
        direction = self.direction
        task = SweepPowerSupply(direction, self.power_supply, self.fast_sweep)

        with self.assertRaises(RuntimeError):
            task.task(self.executor)