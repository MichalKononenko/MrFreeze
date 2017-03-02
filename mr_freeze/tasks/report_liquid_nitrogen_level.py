"""
Describes a task to report the level of liquid nitrogen in the system
"""
from mr_freeze.devices.cryomagnetics_lm510_adapter import CryomagneticsLM510
from time import sleep
from concurrent.futures import Executor
from quantities import Quantity
from mr_freeze.tasks.report_variable_task import ReportVariableTask


class ReportLiquidNitrogenLevel(ReportVariableTask):
    """
    The task to run
    """
    _minimum_time_between_samples = 0.3

    def __init__(self, gauge: CryomagneticsLM510, ln2_channel=2):
        """

        :param gauge: The gauge that reports the nitrogen level
        :param ln2_channel: The channel on that gauge that reports the LN2
            level
        """
        self.gauge = gauge
        self.ln_2_channel = ln2_channel

    @property
    def title(self):
        return "Liquid Nitrogen Level"

    @property
    def _ln2_level(self) -> Quantity:
        """

        :return: The measured liquid nitrogen level
        """
        if self.ln_2_channel == 1:
            return self.gauge.channel_1_measurement
        elif self.ln_2_channel == 2:
            return self.gauge.channel_2_measurement
        else:
            raise RuntimeError("Attempted to measure using unknown channel "
                               "%d" % self.ln_2_channel)

    def _wait_for_minimum_time(self):
        """
        Wait for enough time between the measurements to allow the
        LN2 level meter to return to a state where it can measure again
        """
        sleep(self._minimum_time_between_samples)

    def task(self, executor: Executor) -> Quantity:
        """

        :return: The measured liquid nitrogen level
        """
        level = self._ln2_level
        self._wait_for_minimum_time()
        return level
