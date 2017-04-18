# -*- coding: utf-8 -*-
"""
Describes a task to report the level of liquid nitrogen in the system
"""
from mr_freeze.devices.cryomagnetics_lm510_adapter import CryomagneticsLM510
from time import sleep
from quantities import Quantity, cm
from numpy import nan
from mr_freeze.resources.abstract_store import Store, Variable
from mr_freeze.resources.application_state import LiquidNitrogenLevel
from mr_freeze.tasks.report_variable_task import ReportVariableTask
from mr_freeze.exceptions import NoEchoedCommandFoundError


class ReportLiquidNitrogenLevel(ReportVariableTask):
    """
    The task to run
    """
    title = "Liquid Nitrogen Level"

    _minimum_time_between_samples = 0.3

    def __init__(
            self,
            gauge: CryomagneticsLM510,
            store: Store,
            ln2_channel: int=2
    ) -> None:
        """

        :param gauge: The gauge that reports the nitrogen level
        :param ln2_channel: The channel on that gauge that reports the LN2
            level
        """
        super(ReportLiquidNitrogenLevel, self).__init__(store)
        self.gauge = gauge
        self.ln_2_channel = ln2_channel

    @property
    def variable(self):
        """

        :return: The value of the variable
        """
        try:
            level = self._ln2_level
        except NoEchoedCommandFoundError:
            level = nan * cm
        self._wait_for_minimum_time()
        return level

    @property
    def variable_type(self) -> Variable.__class__:
        """

        :return: The type of variable being returned
        """
        return LiquidNitrogenLevel

    @property
    def _ln2_level(self)-> Quantity:
        """

        :return: The measured liquid nitrogen level
        """
        if self.ln_2_channel == 1:
            return self.gauge.channel_1_measurement
        elif self.ln_2_channel == 2:
            return self.gauge.channel_2_measurement
        else:
            raise RuntimeError(
                "Attempted to measure using unknown channel %d" %
                self.ln_2_channel
            )

    def _wait_for_minimum_time(self):
        sleep(self._minimum_time_between_samples)
