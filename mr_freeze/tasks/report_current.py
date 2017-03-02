"""
Measures the current from the Cryomagnetics 4G power supply
"""
from time import sleep
from quantities import Quantity
from mr_freeze.devices.cryomagnetics_4g_adapter import Cryomagnetics4G
from mr_freeze.tasks.abstract_task import AbstractTask


class ReportCurrent(AbstractTask):
    """
    Reports the current from the Cryomagnetics 4G supply
    """
    def __init__(self, gauge: Cryomagnetics4G):
        """

        :param gauge: The instrument to use for measuring the current
        """
        self.gauge = gauge

    def task(self) -> Quantity:
        """

        :return: The measured current
        """
        current = self.gauge.current
        sleep(0.3)
        return current
