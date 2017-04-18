# -*- coding: utf-8
"""
Contains unit tests for :mod:`mr_freeze.tasks.make_measurement`
"""
import unittest
import unittest.mock as mock
from concurrent.futures import Executor
from mr_freeze.tasks.make_measurement import MakeMeasurement
from mr_freeze.devices.lakeshore_475 import Lakeshore475
from mr_freeze.devices.cryomagnetics_lm510_adapter import CryomagneticsLM510
from mr_freeze.devices.cryomagnetics_4g_adapter import Cryomagnetics4G
from mr_freeze.tasks.report_magnetic_field import ReportMagneticField
from mr_freeze.tasks.report_current import ReportCurrent
from mr_freeze.tasks.report_liquid_nitrogen_level \
    import ReportLiquidNitrogenLevel
from mr_freeze.resources.application_state import Store


class TestMakeMeasurement(unittest.TestCase):
    def setUp(self):
        self.ln2_gauge = mock.MagicMock(spec=CryomagneticsLM510)
        self.magnetometer = mock.MagicMock(spec=Lakeshore475)
        self.power_supply = mock.MagicMock(spec=Cryomagnetics4G)
        self.executor = mock.MagicMock(spec=Executor)  # type: Executor
        self.store = dict()  # type: Store

        self.task = MakeMeasurement(
            self.ln2_gauge, self.magnetometer, self.power_supply, self.store
        )


class TestInitalizer(TestMakeMeasurement):
    def test_initializer(self):
        self.assertIsInstance(
            self.task.ln2_task, ReportLiquidNitrogenLevel
        )
        self.assertIsInstance(
            self.task.current_task, ReportCurrent
        )
        self.assertIsInstance(
            self.task.magnetic_field_task, ReportMagneticField
        )


class TestTask(TestMakeMeasurement):
    def test_task(self):
        self.task.task(self.executor)
        self.assertEqual(
            6,
            self.executor.submit.call_count
        )
