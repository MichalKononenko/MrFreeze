# coding=utf-8
"""
Describes a task to sweep the power supply current up, down, or to 0
"""
from mr_freeze.tasks.abstract_task import AbstractTask
from concurrent.futures import Executor
from mr_freeze.devices.cryomagnetics_4g_adapter import Cryomagnetics4G
from enum import Enum


class SweepPowerSupply(AbstractTask):
    """
    Sweep the power supply to another current value in a particular direction
    """

    class Direction(Enum):
        """
        Represents that allowed directions for the sweep to go
        """
        UP = "UP"
        DOWN = "DOWN"
        ZERO = "ZERO"
        PAUSE = "PAUSE"

    def __init__(
            self, direction: Direction, power_supply: Cryomagnetics4G,
            fast_sweep=False
    ) -> None:
        self.direction = direction
        self.power_supply = power_supply
        self.fast_sweep = fast_sweep

    def task(self, executor: Executor) -> None:
        """

        :param executor: The executor to use for the task
        """
        if self.direction == self.Direction.UP:
            self._sweep_up()
        elif self.direction == self.Direction.DOWN:
            self._sweep_down()
        elif self.direction == self.Direction.ZERO:
            self._sweep_zero()
        elif self.direction == self.Direction.PAUSE:
            self._sweep_pause()
        else:
            raise RuntimeError(
                "No sweep defined for direction %s" % self.direction
            )

    def _sweep_up(self):
        self.power_supply.sweep_up(fast=self.fast_sweep)

    def _sweep_down(self):
        self.power_supply.sweep_down(fast=self.fast_sweep)

    def _sweep_zero(self):
        self.power_supply.sweep_zero(fast=self.fast_sweep)

    def _sweep_pause(self):
        self.power_supply.pause_sweep()

    def __repr__(self):
        return '<%s(direction=%s, power_supply=%s, fast_sweep=%s)>' % (
            self.__class__.__name__, self.direction, self.power_supply,
            self.fast_sweep
        )
