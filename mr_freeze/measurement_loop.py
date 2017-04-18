# coding=utf-8
"""
Describes a loop for measuring instrument values and writing these values to
an application store
"""
import schedule
from concurrent.futures import Executor
from mr_freeze.devices.lakeshore_475 import Lakeshore475
from mr_freeze.devices.cryomagnetics_lm510_adapter import CryomagneticsLM510
from mr_freeze.devices.cryomagnetics_4g_adapter import Cryomagnetics4G
from mr_freeze.resources.application_state import Store
from mr_freeze.tasks.make_measurement import MakeMeasurement


class MeasurementLoop(object):
    """
    Loop for measuring instrument values
    """
    def __init__(
            self,
            power_supply: Cryomagnetics4G,
            level_meter: CryomagneticsLM510,
            magnetometer: Lakeshore475,
            store: Store,
            executor: Executor,
            sample_interval_in_seconds: int,
            scheduler: schedule=schedule
    ) -> None:
        self.power_supply = power_supply
        self.level_meter = level_meter
        self.magnetometer = magnetometer
        self.store = store
        self.executor = executor
        self.sample_interval = sample_interval_in_seconds
        self.scheduler = scheduler

    def run(self) -> None:
        """
        Run the measurement on a particular schedule
        :return:
        """
        self.scheduler.every(self.sample_interval).seconds.do(
            self.run_single_iteration).tag(self.__repr__())

    def run_single_iteration(self) -> None:
        """
        Run a single iteration of the loop
        """
        task = MakeMeasurement(
            self.level_meter, self.power_supply, self.magnetometer, self.store
        )
        task(self.executor)

    def __repr__(self) -> str:
        """

        :return: A representation of this object
        """
        return ''.join(
            (
                self.__class__.__name__,
                '(',
                '%s=%s, ' % ("power_supply", self.power_supply),
                '%s=%s, ' % ("level_meter", self.level_meter),
                '%s=%s, ' % ("magnetometer", self.magnetometer),
                '%s=%s, ' % ("store", self.store),
                '%s=%s, ' % ("executor", self.executor),
                '%s=%s, ' % ("sample_interval", self.sample_interval),
                '%s=%s, ' % ("scheduler", self.scheduler),
                ')'
            )
        )
