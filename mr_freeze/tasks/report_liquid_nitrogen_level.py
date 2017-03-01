"""
Describes a task to report the level of liquid nitrogen in the system
"""
from mr_freeze.devices.cryomagnetics_lm510_adapter import CryomagneticsLM510
from concurrent.futures import Executor, Future
from time import sleep
from quantities import Quantity


class ReportLiquidNitrogenLevel(object):
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

    def __call__(self, executor: Executor) -> Future:
        """

        :param executor: The executor that will run this task
        :return: A wrapper around the task that will return the result
        """
        return executor.submit(self._task)

    @property
    def _ln2_level(self) -> Quantity:
        """

        :return: The measured liquid nitrogen level
        """
        if self.ln_2_channel == 1:
            return self.gauge.level_meter.channel_1_measurement
        elif self.ln_2_channel == 2:
            return self.gauge.level_meter.channel_2_measurement
        else:
            raise RuntimeError("Attempted to measure using unknown channel "
                               "%d" % self.ln_2_channel)

    def _wait_for_minimum_time(self):
        """
        Wait for enough time between the measurements to allow the
        LN2 level meter to return to a state where it can measure again
        """
        sleep(self._minimum_time_between_samples)

    def _task(self) -> Quantity:
        """

        :return: The measured liquid nitrogen level
        """
        level = self._ln2_level
        self._wait_for_minimum_time()
        return level
