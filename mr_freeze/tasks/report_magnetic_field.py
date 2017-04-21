# -*- coding: utf-8 -*-
"""
Describes how to report the magnetic field
"""
from mr_freeze.devices.lakeshore_475 import Lakeshore475
from mr_freeze.resources.abstract_store import Store
from mr_freeze.resources.application_state import MagneticField
from mr_freeze.tasks.report_variable_task import ReportVariableTask
from mr_freeze.exceptions import NoEchoedCommandFoundError
from quantities import Quantity, gauss
from numpy import nan
from time import sleep


class ReportMagneticField(ReportVariableTask):
    """
    Implements a task to return the magnetic field
    """
    title = "Magnetic Field"

    _minimum_time_between_samples = 0.3

    def __init__(self, gauge: Lakeshore475, store: Store) -> None:
        """
        Initialize the task

        :param gauge: The gauge to use for making device measurements
        """
        super(ReportMagneticField, self).__init__(store)
        self.gauge = gauge

    @property
    def variable_type(self):
        """

        :return: The type of variable being reported
        """
        return MagneticField

    @property
    def variable(self) -> Quantity:
        """

        :return: The measured strength of the magnetic field
        """
        try:
            self._wait_for_minimum_time()
            return self.gauge.field
        except NoEchoedCommandFoundError:
            return nan * gauss

    def _wait_for_minimum_time(self):
        sleep(self._minimum_time_between_samples)

    def __repr__(self) -> str:
        """

        :return: A human-friendly representation of this object
        """
        return "{0}(gauge={1}, store={2})".format(
            self.__class__.__name__, self.gauge, self.store
        )
