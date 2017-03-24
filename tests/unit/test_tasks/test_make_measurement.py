import unittest
import unittest.mock as mock
import quantities as pq
from concurrent.futures import Executor
from mr_freeze.tasks.make_measurement import MakeMeasurement
from mr_freeze.devices.lakeshore_475 import Lakeshore475
from mr_freeze.devices.cryomagnetics_lm510_adapter import CryomagneticsLM510
from mr_freeze.devices.cryomagnetics_4g_adapter import Cryomagnetics4G
from mr_freeze.resources.csv_file import CSVFile
from mr_freeze.tasks.report_magnetic_field import ReportMagneticField
from mr_freeze.tasks.report_current import ReportCurrent
from mr_freeze.tasks.report_liquid_nitrogen_level \
    import ReportLiquidNitrogenLevel
from mr_freeze.tasks.write_csv_values import WriteCSVValues


class TestMakeMeasurement(unittest.TestCase):
    def setUp(self):
        self.ln2_gauge = mock.MagicMock(spec=CryomagneticsLM510)
        self.magnetometer = mock.MagicMock(spec=Lakeshore475)
        self.power_supply = mock.MagicMock(spec=Cryomagnetics4G)
        self.csv_file = mock.MagicMock(spec=CSVFile)
        self.executor = mock.MagicMock(spec=Executor)  # type Executor

        self.task = MakeMeasurement(
            self.ln2_gauge, self.magnetometer, self.power_supply,
            self.csv_file
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


class TestWriteValuesToFile(TestMakeMeasurement):
    """
    Replicate a bug where data is not written correctly due to different
    values not being able to be converted to a float
    """
    write_values_task = mock.MagicMock(spec=WriteCSVValues)
    executor = mock.MagicMock(spec=Executor)

    def setUp(self):
        TestMakeMeasurement.setUp(self)
        self.data_to_write = [1, 2 * pq.gauss, "3"]
        self.expected_call_data = ["1", "2.0", "3"]

    def test_write_values(self):
        self.task.write_values_to_file(
            self.data_to_write, self.executor,
            write_values_task=self.write_values_task
        )
        self.assertEqual(
            mock.call(self.task.csv_file, self.expected_call_data),
            self.write_values_task.call_args
        )
