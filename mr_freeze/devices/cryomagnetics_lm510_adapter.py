"""
Contains an adapter for working with the Cryomagnetics LM 510. This object
provides a layer of abstraction between the InstrumentKit implementation of
the device, and a working device
"""
from typing import Optional
from mr_freeze.devices.cryomagnetics_lm510 import CryomagneticsLM510 as \
    _CryomagneticsLM510


class CryomagneticsLM510(object):
    """
    Adapter layer
    """
    _port = '/dev/ttyUSB0'
    _baud_rate = 9600
    _timeout_in_seconds = 1
    _managed_instance = None
    _constructor = _CryomagneticsLM510

    @property
    def port_name(self) -> str:
        return self._port

    @port_name.setter
    def port_name(self, new_port_name: str):
        self._port = new_port_name

    @property
    def baud_rate(self) -> int:
        return self._baud_rate

    @baud_rate.setter
    def baud_rate(self, new_baud_rate: int):
        self._baud_rate = new_baud_rate

    @property
    def timeout_in_seconds(self) -> int:
        return self._timeout_in_seconds

    @timeout_in_seconds.setter
    def timeout_in_seconds(self, new_timeout: int):
        self._timeout_in_seconds = new_timeout

    @property
    def _level_meter(self) -> Optional[_CryomagneticsLM510]:
        """

        :return:
        """
        if self._managed_instance is None:
            self._managed_instance = self._constructor.open_serial(
                port=self.port_name, baud=self.baud_rate
            )
        return self._managed_instance

    @property
    def channel_1_measurement(self):
        return self._level_meter.channel_1_measurement

    @property
    def channel_2_measurement(self):
        return self._level_meter.channel_2_measurement
