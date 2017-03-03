import logging
import signal
from time import sleep
from concurrent.futures import Executor, ThreadPoolExecutor
from mr_freeze.resources.csv_file import CSVFile
from mr_freeze.devices.cryomagnetics_lm510_adapter import CryomagneticsLM510
from mr_freeze.devices.lakeshore_475 import Lakeshore475
from mr_freeze.devices.cryomagnetics_4g_adapter import Cryomagnetics4G
from mr_freeze.tasks.report_liquid_nitrogen_level import ReportLiquidNitrogenLevel
from mr_freeze.tasks.report_magnetic_field import ReportMagneticField
from mr_freeze.tasks.report_current import ReportCurrent
from mr_freeze.tasks.write_csv_title import WriteCSVTitle
from mr_freeze.tasks.make_measurement import MakeMeasurement

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class MainLoop(object):
    """
    Run the application. Takes commands in from the application parser
    """
    variables_to_report = {
        ReportLiquidNitrogenLevel,
        ReportCurrent,
        ReportMagneticField
    }

    should_run = True

    def __init__(
            self, csv_file_path: str, ln2_gauge_port: str,
            magnetometer_port: str, power_supply_port: str,
            time_between_reports: int, task_timeout: int

    ):
        self.csv_file = CSVFile(csv_file_path, self.variables_to_report)

        self.ln2_gauge = CryomagneticsLM510()
        self.ln2_gauge.port_name = ln2_gauge_port

        self.magnetometer = Lakeshore475()
        self.magnetometer.magnetometer_address = magnetometer_port

        self.power_supply = Cryomagnetics4G()
        self.power_supply.port_name = power_supply_port

        self.polling_interval = time_between_reports
        self.timeout = task_timeout

    @classmethod
    def interrupt(cls):
        log.info("Caught interrupt signal, exiting")
        cls.should_run = False

    def run(self):
        with ThreadPoolExecutor() as executor:
            self._write_title(executor)
            self._run_loop(executor)

    def _write_title(self, executor: Executor):
        task = WriteCSVTitle(self.csv_file)
        task(executor).result(self.timeout)
        log.debug("Wrote title to csv file %s", self.csv_file)

    def _run_loop(self, executor: Executor):
        while self.should_run:
            log.debug("Measuring variables")
            task = MakeMeasurement(
                self.ln2_gauge, self.power_supply, self.magnetometer,
                self.csv_file, self.timeout
            )
            task(executor).result(self.timeout)
            log.debug("Measurement completed. Waiting for time between "
                      "reports")
            sleep(self.polling_interval)

