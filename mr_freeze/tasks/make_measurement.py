# -*- coding: utf-8 -*-
"""
Contains a task that makes a single measurement on the current, cryogen
level, and magnetic field. This task associates these values with a date,
and writes the numbers down as a single line in a CSV file
"""
import logging
from quantities import Quantity
from typing import Iterable, Any, Optional, List
from concurrent.futures import Executor, Future
from mr_freeze.tasks.abstract_task import AbstractTask
from mr_freeze.tasks.report_current import ReportCurrent
from mr_freeze.tasks.report_magnetic_field import ReportMagneticField
from mr_freeze.tasks.write_csv_values import WriteCSVValues
from mr_freeze.tasks.get_current_date import GetCurrentDate
from mr_freeze.tasks.report_liquid_helium_level import ReportLiquidHeliumLevel
from mr_freeze.tasks.report_liquid_nitrogen_level \
    import ReportLiquidNitrogenLevel
from mr_freeze.devices.lakeshore_475 import Lakeshore475 as _Lakeshore475
from mr_freeze.devices.cryomagnetics_4g_adapter \
    import Cryomagnetics4G as _Cryomagnetics4G
from mr_freeze.devices.cryomagnetics_lm510_adapter \
    import CryomagneticsLM510 as _CryomagneticsLM510
from mr_freeze.resources.csv_file import CSVFile as _CSVFile
from mr_freeze.resources.application_state import Store
from mr_freeze.tasks.write_to_pipe import WriteToPipe
from mr_freeze.resources.measurement_pipe import Pipe
from mr_freeze.resources.application_state import LiquidHeliumLevel
from mr_freeze.resources.application_state import LiquidNitrogenLevel
from mr_freeze.resources.application_state import Current
from mr_freeze.resources.application_state import MagneticField

log = logging.getLogger(__name__)


class MakeMeasurement(AbstractTask):
    """
    Run a single measurement, and write the results
    """
    VARIABLE_ORDER = [
        None, LiquidNitrogenLevel, LiquidHeliumLevel, Current, MagneticField
    ]

    def __init__(
            self,
            level_meter: _CryomagneticsLM510,
            current_gauge: _Cryomagnetics4G,
            gaussmeter: _Lakeshore475,
            csv_file: _CSVFile,
            pipe: Pipe,
            store: Store,
            timeout: int=10) -> None:
        """

        :param level_meter: The gauge used to measure liquid nitrogen
        :param current_gauge: The gauge used to measure electrical current
        going into the cryostat
        :param gaussmeter: The gauge used to measure the magnetic field in
        the cryostat
        :param csv_file: A representation of a comma-separated values (CSV)
        file, to which measured values will be written
        :param pipe: The JSON file to which the latest sampled values are to be
        written
        :param timeout: The amount of elapsed time in seconds before a task
        will be considered dead. The default is 10 seconds
        """
        self.ln2_task = ReportLiquidNitrogenLevel(level_meter)
        self.current_task = ReportCurrent(current_gauge)
        self.magnetic_field_task = ReportMagneticField(gaussmeter)
        self.get_date_task = GetCurrentDate()

        self.report_helium_task = ReportLiquidHeliumLevel(level_meter)

        self.pipe = pipe
        self.store = store

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
        lhe_level = self.report_helium_task(executor)  # type: Future

        values_to_write = [
            self._get_result(v) for v in
            [
                get_date, ln2_level, lhe_level, current, magnetic_field
            ]
        ]

        self.write_values_to_file(values_to_write, executor)
        self.write_values_to_pipe(values_to_write, executor)
        self.write_values_to_store(values_to_write)

    def write_values_to_file(self, values: Iterable, executor: Executor,
                             write_values_task=WriteCSVValues) -> None:
        """
        Appends the latest measurements to the CSV file

        :param values: The measured values to write
        :param executor: The executor to be used when evaluating the task
        :param write_values_task: The constructor for the task to write the
        values
        """
        writeable_values = [
            self._prepare_value_for_writing(value) for value in values
        ]

        write_values_task = write_values_task(
            self.csv_file, writeable_values
        )
        write_values_task(executor).result(self.timeout)

    def write_values_to_pipe(
            self, values_to_write: Iterable,
            executor: Executor, task: AbstractTask.__class__=WriteToPipe
    ) -> None:
        """
        Write the latest measurement to the JSON file

        :param values_to_write: The measured values to be written to the file
        :param executor: The executor to be used in running this task
        :param task: The task to be created to write the files
        """

        values_to_write = self._prepare_values_for_pipe(values_to_write)

        writing_task = task(self.pipe, values_to_write)
        writing_task(executor).result(self.timeout)

    def write_values_to_store(self, values_to_write: List):
        """

        :param values_to_write: The values to be written to the store
        :return:
        """
        for index in range(0, len(values_to_write)):
            self.store[self.VARIABLE_ORDER[index]] = values_to_write[index]

    def _get_result(self, value: Future) -> Optional[Any]:
        """
        Evaluate a particular task and return the result

        :param Future value: The task that is to be evaluated
        :return: The return value of the underlying task
        """
        result = value.result(self.timeout)

        log.debug("Received result %s from task %s" % (result, value))

        return result

    @staticmethod
    def _strip_quantity(quantity: Quantity) -> str:
        return str(float(quantity))

    @staticmethod
    def _prepare_value_for_writing(value: object) -> str:
        if isinstance(value, Quantity):
            return MakeMeasurement._strip_quantity(value)
        else:
            return str(value)

    @staticmethod
    def _prepare_values_for_pipe(values_to_write) -> Iterable:
        task_order = [
            GetCurrentDate,
            ReportLiquidNitrogenLevel,
            ReportLiquidHeliumLevel,
            ReportCurrent,
            ReportMagneticField
        ]

        return zip(task_order, values_to_write)
