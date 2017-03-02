from concurrent.futures import Executor, Future
from mr_freeze.tasks.abstract_task import AbstractTask
from mr_freeze.tasks.report_current import ReportCurrent
from mr_freeze.tasks.report_magnetic_field import ReportMagneticField
from mr_freeze.tasks.write_csv_values import WriteCSVValues
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

        values_to_write = (
            float(value.result(self.timeout))
            for value in {ln2_level, current, magnetic_field}
        )
        write_values_task = WriteCSVValues(
            self.csv_file, values_to_write
        )
        write_values_task(executor).result(self.timeout)
