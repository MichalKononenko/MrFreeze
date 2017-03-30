# -*- coding: utf-8 -*-
"""
Describes a task to report the level of liquid helium in the system
"""
import logging
import numpy as np
from time import sleep
from concurrent.futures import Executor
from quantities import Quantity, cm
from mr_freeze.devices.cryomagnetics_lm510_adapter import CryomagneticsLM510
from mr_freeze.exceptions import DeviceCommunicationError
from mr_freeze.tasks.report_variable_task import ReportVariableTask

log = logging.getLogger(__name__)


class ReportLiquidHeliumLevel(ReportVariableTask):
    """
    The task to report the amount of liquid helium in the cryostat
    """
    title = "Liquid Helium Level"
    _minimum_time_between_samples = 0.3

    def __init__(self, gauge: CryomagneticsLM510, lhe_channel: int=1) -> None:
        """

        :param gauge: The gauge that reports the helium level
        :param lhe_channel: The channel on the gauge that reports the liquid
            helium level
        """
        log.debug("Initialized task to report liquid helium %s" % self)
        self.gauge = gauge
        self.lhe_channel = lhe_channel

    def task(self, executor: Executor) -> Quantity:
        """

        :param executor: The executor which will be used to run the task
        :return: The measured helium level. Returns NaN if it cannot be
        obtained
        """
        try:
            level = self._lhe_level
        except DeviceCommunicationError as error:
            log.error(error)
            level = np.nan * cm
        self._wait_for_minimum_time()
        return level

    @property
    def _lhe_level(self) -> Quantity:
        """

        :return: The liquid helium level
        """
        if self.lhe_channel == 1:
            return self.gauge.channel_1_measurement
        elif self.lhe_channel == 2:
            return self.gauge.channel_2_measurement
        else:
            raise RuntimeError(
                "Attempted to measure using unknown channel "
                "%d" % self.lhe_channel)

    def _wait_for_minimum_time(self):
        sleep(self._minimum_time_between_samples)
