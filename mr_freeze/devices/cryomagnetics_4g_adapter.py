"""
Provides an abstraction layer for the Cryomagnetics 4G power supply
implemented in InstrumentKit. This decouples InstrumentKit implementations
from further business logic.

.. note::
    Since the Cryomagnetics 4G Power Supply and the Cryomagnetics LM 510
    level meter both inherit from
    :class:`instruments.abstract_instruments.Instrument`, they shouldn't be
    considered as types that are "owned" by this application. All I/O for
    the device should go through this adapter layer.
"""
import numpy as np
from typing import Optional
from quantities import Quantity, gauss
from mr_freeze.exceptions import NoEchoedCommandFoundError
from mr_freeze.devices.cryomagnetics_4g import Cryomagnetics4G as \
    _Cryomagnetics4G


class Cryomagnetics4G(object):
    """
    Provide the abstraction layer
    """
    _port = '/dev/ttyUSB0'
    _baud_rate = 9600
    _managed_instance = None

    null_value = np.nan * gauss

    def __init__(self, constructor=_Cryomagnetics4G):
        """

        :param constructor: The class to use for creating an instance of
        the power supply. By default, this is the implementation of
        Cryomagnetics 4G power supply provided by InstrumentKit. This value
        should only be overwritten during testing
        """
        self._constructor = constructor

    @property
    def port_name(self) -> str:
        """

        :return: The port to which this power supply is attached
        """
        return self._port

    @port_name.setter
    def port_name(self, new_port: str):
        """

        :param new_port: The desired port that the power supply will be
            attached to
        """
        self._port = new_port

    @property
    def baud_rate(self) -> int:
        """

        :return: The baud rate (bits per second transfer rate) between this
            machine and the device. The baud rate setting must be the same on
            both the machine running this application, and on the device,
            in order to allow communication.
        """
        return self._baud_rate

    @baud_rate.setter
    def baud_rate(self, baud: int):
        """

        :param baud: The new desired baud rate
        """
        self._baud_rate = baud

    @property
    def _power_supply(self) -> Optional[_Cryomagnetics4G]:
        """

        :return: The power supply with the required parameters
        """
        if self._managed_instance is None:
            self._managed_instance = self._constructor.open_serial(
                port=self.port_name, baud=self.baud_rate
            )
        return self._managed_instance

    @property
    def current(self) -> Quantity:
        """

        :return: The current that the power supply has measured
        """
        try:
            current = self._power_supply.current
        except NoEchoedCommandFoundError:
            current = self.null_value

        return current if current is not None else self.null_value
