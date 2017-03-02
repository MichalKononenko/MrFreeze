"""
Describes how to report the magnetic field
"""
from time import sleep
from mr_freeze.devices.lakeshore_475 import Lakeshore475
from mr_freeze.tasks.abstract_task import AbstractTask


class ReportMagneticField(AbstractTask):
    """
    Implements a task to return the magnetic field
    """
    _minimum_time_between_samples = 0.3

    def __init__(self, gauge: Lakeshore475):
        """
        Initialize the task

        :param gauge: The gauge to use for making device measurements
        """
        self.gauge = gauge

    @property
    def _field_strength(self):
        """

        :return: The measured strength of the magnetic field
        """
        return self.gauge.field

    def _wait_for_minimum_time(self):
        """
        Delay execution, allowing the unit to reset itself to a state ready
        to report the pressure again
        """
        sleep(self._minimum_time_between_samples)

    def task(self) -> float:
        """

        :return: The measured pressure
        """
        field_strength = self._field_strength
        self._wait_for_minimum_time()

        return field_strength
