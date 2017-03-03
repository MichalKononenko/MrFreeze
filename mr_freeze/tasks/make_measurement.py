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


class MakeMeasurement(AbstractTask):
    """
    Run a single measurement, and write the results
    """

    def __init__(self, ln2_gauge, current_gauge, gaussmeter,
                 csv_file, timeout=10):
        self.ln2_task = ReportLiquidNitrogenLevel(ln2_gauge)
        self.current_task = ReportCurrent(current_gauge)
        self.magnetic_field_task = ReportMagneticField(gaussmeter)
        self.get_date_task = GetCurrentDate()
        self.csv_file = csv_file

        self.timeout = timeout

    def task(self, executor: Executor):
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