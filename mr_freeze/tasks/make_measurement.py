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
from mr_freeze.tasks.update_store import UpdateStore
from mr_freeze.devices.lakeshore_475 import Lakeshore475 as _Lakeshore475
from mr_freeze.devices.cryomagnetics_4g_adapter \
    import Cryomagnetics4G as _Cryomagnetics4G
from mr_freeze.devices.cryomagnetics_lm510_adapter \
    import CryomagneticsLM510 as _CryomagneticsLM510
from mr_freeze.resources.csv_file import CSVFile as _CSVFile
from mr_freeze.resources.application_state import Store
from mr_freeze.tasks.write_to_pipe import WriteToPipe
from mr_freeze.resources.measurement_pipe import Pipe

log = logging.getLogger(__name__)


class MakeMeasurement(AbstractTask):
    """
    Run a single measurement, and write the results
    """

    def __init__(
            self,
            level_meter: _CryomagneticsLM510,
            current_gauge: _Cryomagnetics4G,
            gaussmeter: _Lakeshore475,
            store: Store,
            timeout: int=10) -> None:
        """

        :param level_meter: The gauge used to measure liquid nitrogen
        :param current_gauge: The gauge used to measure electrical current
        going into the cryostat
        :param gaussmeter: The gauge used to measure the magnetic field in
        the cryostat
        :param timeout: The amount of elapsed time in seconds before a task
        will be considered dead. The default is 10 seconds
        """
        self.ln2_task = ReportLiquidNitrogenLevel(level_meter)
        self.current_task = ReportCurrent(current_gauge)
        self.magnetic_field_task = ReportMagneticField(gaussmeter)
        self.get_date_task = GetCurrentDate()

        self.report_helium_task = ReportLiquidHeliumLevel(level_meter)

        self.store = store

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

        self.write_values_to_store(values_to_write, executor)

    def write_values_to_store(self, values_to_write: List, executor: Executor):
        """

        :param values_to_write: The values to be written to the store
        :param executor: The Executor on which the store update task will be
            executed
        :return:
        """
        update_values_task = UpdateStore(
            self.store,
            new_lhe_level=values_to_write[2],
            new_current=values_to_write[3],
            new_ln2_level=values_to_write[1],
            new_magnetic_field=values_to_write[4]
        )
        task = update_values_task(executor)
        task.result(self.timeout)

    def _get_result(self, value: Future) -> Optional[Any]:
        """
        Evaluate a particular task and return the result

        :param Future value: The task that is to be evaluated
        :return: The return value of the underlying task
        """
        result = value.result(self.timeout)

        log.debug("Received result %s from task %s" % (result, value))

        return result
