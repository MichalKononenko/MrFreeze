"""
Adapter for the power supply
"""
from mr_freeze.devices.cryomagnetics_4g import Cryomagnetics4G as \
    _Cryomagnetics4G
from typing import Optional


class Cryomagnetics4G(object):
    _port = '/dev/ttyUSB0'
    _baud_rate = 9600
    _managed_instance = None
    _constructor = _Cryomagnetics4G

    @property
    def port_name(self) -> str:
        return self._port

    @port_name.setter
    def port_name(self, new_port: str):
        self._port = new_port

    @property
    def baud_rate(self) -> int:
        return self._baud_rate

    @baud_rate.setter
    def baud_rate(self, baud: int):
        self._baud_rate = baud

    @property
    def _power_supply(self) -> Optional[_Cryomagnetics4G]:
        if self._managed_instance is None:
            self._managed_instance = self._constructor.open_serial(
                port=self.port_name, baud=self.baud_rate
            )
        return self._managed_instance

    @property
    def current(self):
        return self._power_supply.current