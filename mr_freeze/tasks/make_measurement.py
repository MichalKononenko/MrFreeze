from concurrent.futures import Executor, Future
from quantities import Quantity
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
    _executor = None

    def __init__(self, ln2_gauge, current_gauge, gaussmeter,
                 csv_file, timeout=10):
        self.ln2_task = ReportLiquidNitrogenLevel(ln2_gauge)
        self.current_task = ReportCurrent(current_gauge)
        self.magnetic_field_task = ReportMagneticField(gaussmeter)
        self.csv_file = csv_file

        self.timeout = timeout

    def __call__(self, executor: Executor) -> Future:
        self._executor = executor
        return executor.submit(self.task)

    def task(self):
        pressure = self.ln2_task(
            self._executor
        ).result(self.timeout)  # type: Quantity
        current = self.current_task(
            self._executor
        ).result(self.timeout)  # type: Quantity
        magnetic_field = self.magnetic_field_task(
            self._executor
        ).result(self.timeout)  # type: Quantity

        values_to_write = (
            float(value) for value in {pressure, current, magnetic_field}
        )
        write_values_task = WriteCSVValues(
            self.csv_file, values_to_write
        )
        write_values_task(self._executor).result(self.timeout)
