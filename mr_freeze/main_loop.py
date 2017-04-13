# -*- coding: utf-8 -*-
"""
Contains the main application loop, which iterates for the lifetime of the
application, and reports the required variables
"""
import logging
from time import sleep
from multiprocessing import cpu_count
from concurrent.futures import Executor, ThreadPoolExecutor
from mr_freeze.resources.csv_file import CSVFile
from mr_freeze.resources.measurement_pipe import Pipe
from mr_freeze.devices.cryomagnetics_lm510_adapter import CryomagneticsLM510
from mr_freeze.devices.lakeshore_475 import Lakeshore475
from mr_freeze.devices.cryomagnetics_4g_adapter import Cryomagnetics4G
from mr_freeze.tasks.report_liquid_helium_level import ReportLiquidHeliumLevel
from mr_freeze.tasks.report_liquid_nitrogen_level import ReportLiquidNitrogenLevel
from mr_freeze.tasks.report_magnetic_field import ReportMagneticField
from mr_freeze.tasks.report_current import ReportCurrent
from mr_freeze.tasks.write_csv_title import WriteCSVTitle
from mr_freeze.tasks.make_measurement import MakeMeasurement
from mr_freeze.tasks.get_current_date import GetCurrentDate
from mr_freeze.resources.application_state import Store

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class MainLoop(object):
    """
    Run the application. Takes commands in from the application parser
    """
    variables_to_report = [
        GetCurrentDate,
        ReportLiquidNitrogenLevel,
        ReportLiquidHeliumLevel,
        ReportCurrent,
        ReportMagneticField
    ]

    should_run = True

    def __init__(
            self, csv_file_path: str, pipe_file_path: str, ln2_gauge_port: str,
            magnetometer_port: str, power_supply_port: str,
            time_between_reports: int, task_timeout: int

    ) -> None:
        """
        Instantiate the resources required for the application loop based on
        the arguments given in the command line

        :param csv_file_path: The path to the output CSV file
        :param pipe_file_path: The path to the output JSON file
        :param ln2_gauge_port: The name of the port on which the liquid
        nitrogen level meter is connected
        :param magnetometer_port: The name of the port on which the
        Lakeshore 475 magnetometer is connected
        :param power_supply_port: The name of the port on which the
        Cryomagnetics 4G power supply is connected
        :param time_between_reports: The time in seconds that should elapse
        before the variables are measured
        :param task_timeout: The amount of time to wait before declaring a
        task dead
        """
        self.csv_file = CSVFile(csv_file_path, self.variables_to_report)
        self.pipe = Pipe(pipe_file_path)

        self.ln2_gauge = CryomagneticsLM510()
        self.ln2_gauge.port_name = ln2_gauge_port

        self.magnetometer = Lakeshore475()
        self.magnetometer.port_name = magnetometer_port

        self.power_supply = Cryomagnetics4G()
        self.power_supply.port_name = power_supply_port

        self.polling_interval = time_between_reports
        self.timeout = task_timeout

        self.get_date_task = GetCurrentDate()

        self.executor = ThreadPoolExecutor(5 * cpu_count())
        self.store = Store(self.executor)

    def interrupt(self) -> None:
        """
        Stop the application
        """
        log.info("Caught interrupt signal, exiting")
        self.should_run = False

    def run(self) -> None:
        """
        Write down the title line for the output CSV file, and then start
        the variable measurement loop
        """
        self._write_title(self.executor)
        self._run_loop(self.executor)

    def _write_title(self, executor: Executor) -> None:
        """
        Write the title to the CSV file
        :param executor: The executor to use for writing these values
        """
        task = WriteCSVTitle(self.csv_file)
        task(executor).result(self.timeout)
        log.debug("Wrote title to csv file %s", self.csv_file)

    def _run_loop(self, executor: Executor) -> None:
        """
        Run the loop

        :param executor: The executor with which the loop will be run
        """
        while self.should_run:
            log.debug("Measuring variables")
            task = MakeMeasurement(
                self.ln2_gauge, self.power_supply, self.magnetometer,
                self.csv_file, self.pipe, self.store, self.timeout
            )
            task(executor).result(self.timeout)
            log.debug("Measurement completed. Waiting for time between "
                      "reports")
            sleep(self.polling_interval)
