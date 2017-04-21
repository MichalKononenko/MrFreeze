# -*- coding: utf-8 -*-
"""
Contains a task that makes a single measurement on the current, cryogen
level, and magnetic field. This task associates these values with a date,
and writes the numbers down as a single line in a CSV file
"""
import logging
from concurrent.futures import Executor, Future
from mr_freeze.tasks.abstract_task import AbstractTask
from mr_freeze.tasks.report_current import ReportCurrent
from mr_freeze.tasks.report_magnetic_field import ReportMagneticField
from mr_freeze.tasks.report_liquid_helium_level import ReportLiquidHeliumLevel
from mr_freeze.tasks.report_liquid_nitrogen_level \
    import ReportLiquidNitrogenLevel
from mr_freeze.devices.lakeshore_475 import Lakeshore475 as _Lakeshore475
from mr_freeze.devices.cryomagnetics_4g_adapter \
    import Cryomagnetics4G as _Cryomagnetics4G
from mr_freeze.devices.cryomagnetics_lm510_adapter \
    import CryomagneticsLM510 as _CryomagneticsLM510
from mr_freeze.resources.application_state import Store

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
            store: Store) -> None:
        """

        :param level_meter: The gauge used to measure liquid nitrogen
        :param current_gauge: The gauge used to measure electrical current
        going into the cryostat
        :param gaussmeter: The gauge used to measure the magnetic field in
        the cryostat
        """
        self.ln2_task = ReportLiquidNitrogenLevel(level_meter, store)
        self.current_task = ReportCurrent(current_gauge, store)
        self.magnetic_field_task = ReportMagneticField(gaussmeter, store)
        self.report_helium_task = ReportLiquidHeliumLevel(level_meter, store)
        self.store = store

    def task(self, executor: Executor) -> None:
        """
        Measure the variables and write them to the CSV file

        :param executor: The executor to use for making the measurement
        :return:
        """
        self.ln2_task(executor)  # type: Future
        self.current_task(executor)  # type: Future
        self.magnetic_field_task(executor)  # type: Future
        self.report_helium_task(executor)  # type: Future
