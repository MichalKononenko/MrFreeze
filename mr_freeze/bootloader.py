# coding=utf-8
"""
Module responsible for starting the application.
"""
import logging
import sys
from multiprocessing import cpu_count
from typing import Iterable
from concurrent.futures import ThreadPoolExecutor
from mr_freeze.devices.lakeshore_475 import Lakeshore475
from mr_freeze.devices.cryomagnetics_lm510_adapter import CryomagneticsLM510
from mr_freeze.devices.cryomagnetics_4g_adapter import Cryomagnetics4G
from mr_freeze.cli_argument_parser import parser
from mr_freeze.config_file_parser import ConfigFileParser
from mr_freeze.resources.application_state import Store
from mr_freeze.ui.ui_loader import Main as GUI
from mr_freeze.measurement_loop import MeasurementLoop

log = logging.getLogger(__name__)


class Application(object):
    """
    Base class for the application
    """
    _executor = ThreadPoolExecutor(5 * cpu_count())
    _store = Store(_executor)

    def __init__(self, command_line_arguments: Iterable[str]=sys.argv):
        self.config_file_parser = ConfigFileParser()
        self._cli_arguments = parser.parse_args(command_line_arguments)

        self._gaussmeter = self._configure_gaussmeter()
        self._level_meter = self._configure_level_meter()
        self._power_supply = self._configure_power_supply()

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
            sample_interval_in_seconds=30
        )
        loop.run()

    def start_gui(self, gui_builder: GUI.__class__=GUI) -> None:
        """
        Start the application GUI

        :param gui_builder: The class to use to start the GUI
        """
        gui = gui_builder(self._store)
        gui.show()

    def start(self):
        """
        Start the measurement loop and the GUI

        :return:
        """
        self.start_gui()
        self.start_loop()

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
