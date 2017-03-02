"""
Describes how to report the magnetic field
"""
from time import sleep
from mr_freeze.devices.lakeshore_475 import Lakeshore475
from concurrent.futures import Executor, Future


class ReportMagneticField(object):
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

    def __call__(self, executor: Executor) -> Future:
        """
        Submit this task to an executor for execution

        :param executor: The executor to use
        :return A wrapper around the task that was executed. Calling
        :meth:`Future.result` on this will return the result of the task
        """
        return executor.submit(self._task)

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

    def _task(self) -> float:
        """

        :return: The measured pressure
        """
        field_strength = self._field_strength
        self._wait_for_minimum_time()

        return field_strength
