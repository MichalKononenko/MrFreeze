# -*- coding: utf-8
"""
Measures the current from the Cryomagnetics 4G power supply
"""
from time import sleep
import numpy as np
from quantities import A
from mr_freeze.devices.cryomagnetics_4g_adapter import Cryomagnetics4G
from mr_freeze.tasks.report_variable_task import ReportVariableTask
from mr_freeze.resources.abstract_store import Store
from mr_freeze.resources.application_state import Current
from mr_freeze.exceptions import NoEchoedCommandFoundError


class ReportCurrent(ReportVariableTask):
    """
    Reports the current from the Cryomagnetics 4G supply
    """
    title = "Current"

    def __init__(self, gauge: Cryomagnetics4G, store: Store) -> None:
        """

        :param gauge: The instrument to use for measuring the current
        """
        super(ReportCurrent, self).__init__(store)
        self.gauge = gauge

    @property
    def variable_type(self):
        """

        :return: The variable reported by this task
        """
        return Current

    @property
    def variable(self):
        """

        :return: The measured current
        """
        try:
            current = self.gauge.current
        except NoEchoedCommandFoundError:
            current = np.nan * A
        sleep(0.3)
        return current
