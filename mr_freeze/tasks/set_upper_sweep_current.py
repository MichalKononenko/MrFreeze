# coding=utf-8
"""
Set the upper sweep current
"""
from quantities import Quantity
from concurrent.futures import Executor
from mr_freeze.tasks.abstract_task import AbstractTask
from mr_freeze.devices.cryomagnetics_4g_adapter import Cryomagnetics4G


class SetUpperSweepCurrent(AbstractTask):
    """
    Sets the upper sweep current
    """
    def __init__(
            self,
            sweep_current: Quantity,
            power_supply: Cryomagnetics4G
    ) -> None:
        self.sweep_current = sweep_current
        self.power_supply = power_supply

    def task(self, executor: Executor) -> None:
        """

        :param executor: The executor with which this task is to be done
        """
        self.power_supply.upper_sweep_current = self.sweep_current

    def __repr__(self):
        return '<%s(sweep_current=%s, power_supply=%s)>' % (
            self.__class__.__name__, self.sweep_current, self.power_supply
        )
