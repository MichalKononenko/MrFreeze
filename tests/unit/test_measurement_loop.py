# coding=utf-8
"""
Contains unit tests for :mod:`mr_freeze.measurement_loop`
"""
import unittest
import unittest.mock as mock
import schedule
from concurrent.futures import Executor
from mr_freeze.measurement_loop import MeasurementLoop
from mr_freeze.devices.cryomagnetics_lm510_adapter import CryomagneticsLM510
from mr_freeze.devices.cryomagnetics_4g_adapter import Cryomagnetics4G
from mr_freeze.devices.lakeshore_475 import Lakeshore475
from mr_freeze.resources.application_state import Store


class TestMeasurementLoop(unittest.TestCase):
    """
    Contains unit tests for the measuring loop
    """
    def setUp(self):
        self.level_meter = mock.MagicMock(
            spec=CryomagneticsLM510
        )  # type: CryomagneticsLM510
        self.power_supply = mock.MagicMock(
            spec=Cryomagnetics4G
        )  # type: Cryomagnetics4G
        self.gaussmeter = mock.MagicMock(
            spec=Lakeshore475
        )  # type: Lakeshore475
        self.store = dict()  # type: Store
        self.executor = mock.MagicMock(spec=Executor)  # type: Executor
        self.sample_interval = 10
        self.scheduler = mock.MagicMock(spec=schedule)

        self.loop = MeasurementLoop(
            self.power_supply, self.level_meter, self.gaussmeter,
            self.store, self.executor, self.sample_interval, self.scheduler
        )


class TestRun(TestMeasurementLoop):
    """
    Contains unit tests for the run method
    """
    def test_run(self):
        self.loop.run()
        self.assertEqual(
            mock.call(self.loop.__repr__()),
            self.scheduler.every(self.sample_interval).seconds.do(
                self.loop.run_single_iteration).tag.call_args
        )


class TestRunSingleIteration(TestMeasurementLoop):
    """
    Contains unit tests for running a single iteration of the loop
    """
    def test_run_single_iteration(self):
        self.loop.run_single_iteration()
        self.assertTrue(self.executor.submit.called)
