# coding=utf-8
"""
Contains unit tests for the bootloader
"""
import unittest
import unittest.mock as mock
from mr_freeze.measurement_loop import MeasurementLoop
from mr_freeze.bootloader import Application


class TestApplication(unittest.TestCase):
    def setUp(self):
        self.command_line_arguments = (
                "--gaussmeter-address=/dev/ttyUSB0",
                '--power-supply-address=/dev/ttyUSB1',
                '--ln2-gauge-address=/dev/ttyUSB2'
            )
        self.app = Application(self.command_line_arguments)


class TestStartLoop(TestApplication):
    """
    Tests that the loop starts correctly
    """
    def setUp(self):
        TestApplication.setUp(self)
        self.task_builder = mock.MagicMock(spec=MeasurementLoop.__class__)

    def test_start_loop(self):
        self.app.start_loop(task_builder=self.task_builder)

        self.assertEqual(
            mock.call(
                magnetometer=self.app._gaussmeter,
                level_meter=self.app._level_meter,
                power_supply=self.app._power_supply,
                store=self.app._store,
                executor=self.app._executor,
                sample_interval_in_seconds=30
            ),
            self.task_builder.call_args
        )

        self.assertTrue(
            self.task_builder().run.called
        )
