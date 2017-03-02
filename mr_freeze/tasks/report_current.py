"""
Measures the current from the Cryomagnetics 4G power supply
"""
from time import sleep
from quantities import Quantity
from concurrent.futures import Executor, Future
from mr_freeze.devices.cryomagnetics_4g_adapter import Cryomagnetics4G


class ReportCurrent(object):
    """
    Reports the current from the Cryomagnetics 4G supply
    """
    def __init__(self, gauge: Cryomagnetics4G):
        """

        :param gauge: The instrument to use for measuring the current
        """
        self.gauge = gauge

    def __call__(self, executor: Executor) -> Future:
        """

        :param executor: The executor to which the task is to be submitted
        :return:
        """
        return executor.submit(self._task)

    def _task(self) -> Quantity:
        """

        :return: The measured current
        """
        current = self.gauge.current
        sleep(0.3)
        return current
