"""
Measures the current from the Cryomagnetics 4G power supply
"""
from time import sleep
from concurrent.futures import Executor
from quantities import Quantity
from mr_freeze.devices.cryomagnetics_4g_adapter import Cryomagnetics4G
from mr_freeze.tasks.report_variable_task import ReportVariableTask


class ReportCurrent(ReportVariableTask):
    """
    Reports the current from the Cryomagnetics 4G supply
    """
    def __init__(self, gauge: Cryomagnetics4G):
        """

        :param gauge: The instrument to use for measuring the current
        """
        self.gauge = gauge

    @property
    def title(self):
        return "Current"

    def task(self, executor: Executor) -> Quantity:
        """

        :return: The measured current
        """
        current = self.gauge.current
        sleep(0.3)
        return current
