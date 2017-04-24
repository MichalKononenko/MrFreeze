# coding=utf-8
"""
Logs the output to the CSV file
"""
import csv
import os
from datetime import datetime
from typing import Dict, Optional, Any, Iterable
from concurrent.futures import Executor
from quantities import Quantity
from mr_freeze.resources.abstract_store import Store, Variable
from mr_freeze.resources.application_state import LiquidHeliumLevel
from mr_freeze.resources.application_state import LiquidNitrogenLevel
from mr_freeze.resources.application_state import MagneticField
from mr_freeze.resources.application_state import Current
from mr_freeze.resources.application_state import LoggingInterval
import schedule


class CurrentDate(Variable):
    """
    Returns the current date as a variable
    """
    def __init__(self, variable_update_executor: Executor):
        super().__init__(datetime.now().isoformat(), variable_update_executor)


class CSVLogger(object):
    """
    Logs the output from a store to a CSV file
    """
    VARIABLE_TITLES = {
        CurrentDate: "Date and Time",
        LiquidHeliumLevel: "Liquid Helium (cm)",
        LiquidNitrogenLevel: "Liquid Nitrogen (cm)",
        MagneticField: "Magnetic Field (cm)",
        Current: "Current (A)"
    }

    VARIABLE_ORDER = (
        CurrentDate,
        LiquidHeliumLevel,
        LiquidNitrogenLevel,
        MagneticField,
        Current
    )

    _writing_mode = 'a+'
    _delimiter = ', '
    _logger_tag = 'log-values'

    def __init__(
            self, store: Store, path_to_csv_file: str, executor: Executor
    ) -> None:
        self.store = store
        self.path = path_to_csv_file
        self.executor = executor

    def start_logging(self, scheduler=schedule) -> None:
        """
        Start the logger
        """
        scheduler.every(self._logging_interval).minutes.do(
            self.write_values
        ).tag(self._logger_tag)

    def stop_logging(self, scheduler=schedule) -> None:
        """
        Stop the logger
        """
        scheduler.clear(self._logger_tag)

    def write_titles(self) -> None:
        """
        Write titles to the file
        """
        with open(self.path, mode=self._writing_mode) as file:
            writer = csv.DictWriter(f=file, fieldnames=self._variable_titles)
            writer.writeheader()

    def write_values(self) -> None:
        """
        Write the current values from the store to the file
        """
        if not os.path.isfile(self.path):
            self.write_titles()

        with open(self.path, mode=self._writing_mode) as file:
            writer = csv.DictWriter(f=file, fieldnames=self._variable_titles)
            writer.writerow(self._values_for_dict_writer)

    @property
    def _logging_interval(self):
        """

        :return: The amount of time that should elapse before making a log
        entry
        """
        return self.store[LoggingInterval].value

    @property
    def _variable_titles(self) -> Iterable[str]:
        return [self.VARIABLE_TITLES[key] for key in self.VARIABLE_ORDER]

    @property
    def _values_from_store(self) -> Dict[Variable, Quantity]:
        """

        :return: The measured values from the store
        """
        return {
            LiquidHeliumLevel: self.store[LiquidHeliumLevel].value,
            LiquidNitrogenLevel: self.store[LiquidNitrogenLevel].value,
            MagneticField: self.store[MagneticField].value,
            Current: self.store[Current].value
        }

    @property
    def _date(self) -> CurrentDate:
        """

        :return: The current date
        """
        return CurrentDate(self.executor)

    @property
    def _variables(self) -> Dict[Variable, Optional[Any]]:
        """
        Merge the two dicts and return the values that are to be written
        :return: The values to be written
        """
        variables = self._values_from_store
        variables[CurrentDate] = self._date.value
        return variables

    @property
    def _values_for_dict_writer(self) -> Dict[str, str]:
        """

        :return: A dictionary with string titles and strings representing
        the value of the variables. This will be written via the CSV dict
        writer to the CSV file
        """
        return {
            self.VARIABLE_TITLES[key]:
                self._process_value(self._variables[key])
            for key in self._variables.keys()
        }

    @staticmethod
    def _process_value(value: Optional[Any]) -> str:
        """
        Cast the value to the correct type. If the value is a quantity,
        strip the unit from it

        :param value: The value to process
        :return: The processed value
        """
        if isinstance(value, Quantity):
            return str(float(value))
        else:
            return str(value)
