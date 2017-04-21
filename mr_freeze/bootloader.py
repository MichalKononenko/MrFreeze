# coding=utf-8
"""
Module responsible for starting the application.
"""
import logging
import sys
import time
import schedule
from PyQt4 import QtGui
from PyQt4.QtCore import QThread
from multiprocessing import cpu_count
from typing import Iterable
from concurrent.futures import ThreadPoolExecutor
from quantities import Quantity
from mr_freeze.devices.lakeshore_475 import Lakeshore475
from mr_freeze.devices.cryomagnetics_lm510_adapter import CryomagneticsLM510
from mr_freeze.devices.cryomagnetics_4g_adapter import Cryomagnetics4G
from mr_freeze.cli_argument_parser import parser
from mr_freeze.config_file_parser import ConfigFileParser
from mr_freeze.resources.application_state import Store, CSVDirectory
from mr_freeze.ui.ui_loader import Main as GUI
from mr_freeze.measurement_loop import MeasurementLoop
from mr_freeze.resources.application_state import LowerSweepCurrent
from mr_freeze.resources.application_state import UpperSweepCurrent
from mr_freeze.resources.application_state import PowerSupply
from mr_freeze.tasks.set_lower_sweep_current import SetLowerSweepCurrent
from mr_freeze.tasks.set_upper_sweep_current import SetUpperSweepCurrent

log = logging.getLogger(__name__)


class Application(object):
    """
    Base class for the application
    """
    _executor = ThreadPoolExecutor(5 * cpu_count())
    _store = Store(_executor)

    def __init__(self, command_line_arguments: Iterable[str]=sys.argv[1:]):
        self.config_file_parser = ConfigFileParser()
        self._cli_arguments = parser.parse_args(command_line_arguments)

        self._gaussmeter = self._configure_gaussmeter()
        self._level_meter = self._configure_level_meter()
        self._power_supply = self._configure_power_supply()
        self._app = QtGui.QApplication(sys.argv)
        self._gui = GUI(self._store)
        self._add_control_listeners_to_store(self._store)
        self._store[PowerSupply] = self._power_supply
        self._store[CSVDirectory].value = self._csv_directory

    def start_loop(
            self,
            task_builder: MeasurementLoop.__class__=MeasurementLoop) -> None:
        """
        Start the main measurement loop

        :param task_builder: The class to be used for creating the task to
        run a loop.
        """
        loop = task_builder(
            magnetometer=self._gaussmeter,
            level_meter=self._level_meter,
            power_supply=self._power_supply,
            store=self._store,
            executor=self._executor,
            sample_interval_in_seconds=10
        )
        loop.run()

    def start(self) -> None:
        """
        Start the measurement loop and the GUI

        :return: The exit code for the application
        """
        loop_thread = self._MeasurementLoopThread()

        if not self._gui_only_mode:
            self.start_loop()
            loop_thread.start()

        self._gui.show()

        return self._app.exec_()

    @property
    def _gaussmeter_address(self) -> str:
        """

        :return: The address of the gaussmeter
        """
        try:
            return self._cli_arguments.gaussmeter_address
        except AttributeError:
            log.info(
                self._make_argument_not_found_message(
                    "gaussmeter_address", self.config_file_parser.config_file
                )
            )

        return self.config_file_parser.gaussmeter_address

    @property
    def _level_meter_address(self) -> str:
        """

        :return: The address of the level meter
        """
        try:
            return self._cli_arguments.ln2_gauge_address
        except AttributeError:
            log.info(
                self._make_argument_not_found_message(
                    "ln2_gauge_address", self.config_file_parser.config_file
                )
            )

        return self.config_file_parser.level_meter_address

    @property
    def _power_supply_address(self) -> str:
        """

        :return:
        """
        try:
            return self._cli_arguments.power_supply_address
        except AttributeError:
            log.info(
                self._make_argument_not_found_message(
                    "power_supply_address", self.config_file_parser.config_file
                )
            )

        return self.config_file_parser.power_supply_address

    @property
    def _gui_only_mode(self) -> bool:
        """

        :return: True if the application was started in GUI only mode
        """
        try:
            return self._cli_arguments.gui_only_mode
        except AttributeError:
            return False

    @property
    def _csv_directory(self) -> str:
        """

        :return: The directory to which the logfile is to be written
        """
        try:
            return self._cli_arguments.csv_file
        except AttributeError:
            return self.config_file_parser.csv_output_directory

    def _add_control_listeners_to_store(self, store: Store):
        """

        :param store: The store to which control listeners are to be added
        :return:
        """
        store[LowerSweepCurrent].listeners.add(
            self._handle_lower_sweep_current_change
        )
        store[UpperSweepCurrent].listeners.add(
            self._handle_upper_sweep_current_change
        )

    def _handle_lower_sweep_current_change(
            self, new_current: Quantity
    ) -> None:
        task = SetLowerSweepCurrent(new_current, self._power_supply)
        task(self._executor)

    def _handle_upper_sweep_current_change(
            self, new_current: Quantity
    ) -> None:
        task = SetUpperSweepCurrent(new_current, self._power_supply)
        task(self._executor)

    @staticmethod
    def _make_argument_not_found_message(argument, config_file):
        return """
        Could not find argument %s in command line arguments.
        Using argument from file %s
        """ % (argument, config_file)

    def _configure_gaussmeter(self) -> Lakeshore475:
        gaussmeter = Lakeshore475()
        gaussmeter.port_name = self._gaussmeter_address
        return gaussmeter

    def _configure_level_meter(self) -> CryomagneticsLM510:
        meter = CryomagneticsLM510()
        meter.port_name = self._level_meter_address
        return meter

    def _configure_power_supply(self) -> Cryomagnetics4G:
        meter = Cryomagnetics4G()
        meter.port_name = self._power_supply_address
        return meter

    class _MeasurementLoopThread(QThread):
        """
        Runs the measurement loop in a separate thread
        """
        def run(self) -> None:
            """
            Run the scheduler
            :return:
            """
            log.info("Starting instrument measurement thread")
            while True:
                schedule.run_pending()
                time.sleep(1)
