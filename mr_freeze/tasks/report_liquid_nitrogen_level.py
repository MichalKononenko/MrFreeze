from mr_freeze.devices.cryomagnetics_lm510_adapter import CryomagneticsLM510
from concurrent.futures import Executor, Future
from time import sleep


class ReportLiquidNitrogenLevel(object):
    _minimum_time_between_samples = 0.3

    def __init__(self, gauge: CryomagneticsLM510, ln2_channel=2):
        self.gauge = gauge
        self.ln_2_channel = ln2_channel

    def __call__(self, executor: Executor) -> Future:
        return executor.submit(self._task)

    @property
    def _ln2_level(self) -> float:
        if self.ln_2_channel == 1:
            return self.gauge.level_meter.channel_1_measurement
        elif self.ln_2_channel == 2:
            return self.gauge.level_meter.channel_2_measurement
        else:
            raise RuntimeError("Attempted to measure using unknown channel "
                               "%d" % self.ln_2_channel)

    def _wait_for_minimum_time(self):
        sleep(self._minimum_time_between_samples)

    def _task(self) -> float:
        level = self._ln2_level
        self._wait_for_minimum_time()
        return level
