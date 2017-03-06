"""
Contains a task that makes a single measurement on the current, cryogen
level, and magnetic field. This task associates these values with a date,
and writes the numbers down as a single line in a CSV file
"""
from quantities import Quantity
from typing import Iterable
from concurrent.futures import Executor, Future
from mr_freeze.tasks.abstract_task import AbstractTask
from mr_freeze.tasks.report_current import ReportCurrent
from mr_freeze.tasks.report_magnetic_field import ReportMagneticField
from mr_freeze.tasks.write_csv_values import WriteCSVValues
from mr_freeze.tasks.get_current_date import GetCurrentDate
from mr_freeze.tasks.report_liquid_nitrogen_level \
    import ReportLiquidNitrogenLevel
from mr_freeze.devices.lakeshore_475 import Lakeshore475 as _Lakeshore475
from mr_freeze.devices.cryomagnetics_4g_adapter \
    import Cryomagnetics4G as _Cryomagnetics4G
from mr_freeze.devices.cryomagnetics_lm510_adapter \
    import CryomagneticsLM510 as _CryomagneticsLM510
from mr_freeze.resources.csv_file import CSVFile as _CSVFile


class MakeMeasurement(AbstractTask):
    """
    Run a single measurement, and write the results
    """

    def __init__(
            self,
            ln2_gauge: _CryomagneticsLM510,
            current_gauge: _Cryomagnetics4G,
            gaussmeter: _Lakeshore475,
            csv_file: _CSVFile,
            timeout: int=10) -> None:
        """

        :param ln2_gauge: The gauge used to measure liquid nitrogen
        :param current_gauge: The gauge used to measure electrical current
        going into the cryostat
        :param gaussmeter: The gauge used to measure the magnetic field in
        the cryostat
        :param csv_file: A representation of a comma-separated values (CSV)
        file, to which measured values will be written
        :param timeout: The amount of elapsed time in seconds before a task
        will be considered dead. The default is 10 seconds
        """
        self.ln2_task = ReportLiquidNitrogenLevel(ln2_gauge)
        self.current_task = ReportCurrent(current_gauge)
        self.magnetic_field_task = ReportMagneticField(gaussmeter)
        self.get_date_task = GetCurrentDate()
        self.csv_file = csv_file
        self.timeout = timeout

    def task(self, executor: Executor) -> None:
        """
        Measure the variables and write them to the CSV file

        :param executor: The executor to use for making the measurement
        :return:
        """
        ln2_level = self.ln2_task(executor)  # type: Future
        current = self.current_task(executor)  # type: Future
        magnetic_field = self.magnetic_field_task(executor)  # type: Future
        get_date = self.get_date_task(executor)  # type: Future

        values_to_write = map(
            self._get_result, [get_date, ln2_level, current, magnetic_field]
        )

        self.write_values_to_file(values_to_write, executor)

    def write_values_to_file(self, values: Iterable, executor: Executor,
                             write_values_task=WriteCSVValues):

        writeable_values = [
            self._prepare_value_for_writing(value) for value in values
        ]

        write_values_task = write_values_task(
            self.csv_file, writeable_values
        )
        write_values_task(executor).result(self.timeout)

    def _get_result(self, value: Future):
        return value.result(self.timeout)

    @staticmethod
    def _strip_quantity(quantity: Quantity):
        return str(float(quantity))

    @staticmethod
    def _prepare_value_for_writing(value: object):
        if isinstance(value, Quantity):
            return MakeMeasurement._strip_quantity(value)
        else:
            return str(value)