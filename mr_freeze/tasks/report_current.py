"""
Measures the current from the Cryomagnetics 4G power supply
"""
from time import sleep
from concurrent.futures import Executor
import numpy as np
from quantities import Quantity, A
from mr_freeze.devices.cryomagnetics_4g_adapter import Cryomagnetics4G
from mr_freeze.tasks.report_variable_task import ReportVariableTask
from mr_freeze.exceptions import NoEchoedCommandFoundError


class ReportCurrent(ReportVariableTask):
    """
    Reports the current from the Cryomagnetics 4G supply
    """
    title = "Current"

    def __init__(self, gauge: Cryomagnetics4G) -> None:
        """

        :param gauge: The instrument to use for measuring the current
        """
        self.gauge = gauge

    def task(self, executor: Executor) -> Quantity:
        """

        :return: The measured current
        """
        try:
            current = self.gauge.current
        except NoEchoedCommandFoundError:
            current = np.nan * A
        sleep(0.3)
        return current
