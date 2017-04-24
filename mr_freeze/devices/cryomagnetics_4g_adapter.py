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
from quantities import Quantity, gauss, amperes
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

    @property
    def upper_sweep_current(self) -> Quantity:
        """

        :return: The upper sweep current
        """
        try:
            current = self._power_supply.upper_sweep_current
        except NoEchoedCommandFoundError:
            current = self.null_value

        return current if current is not None else self.null_value

    @upper_sweep_current.setter
    def upper_sweep_current(self, new_current: Quantity) -> None:
        """

        :param new_current: The new value of the current
        """
        self._assert_valid_current(new_current)
        self._power_supply.upper_sweep_current = new_current

    @property
    def lower_sweep_current(self) -> Quantity:
        """

        :return: The lower sweep current
        """
        try:
            current = self._power_supply.lower_sweep_current
        except NoEchoedCommandFoundError:
            current = self.null_value

        return current if current is not None else self.null_value

    @lower_sweep_current.setter
    def lower_sweep_current(self, new_current: Quantity) -> None:
        """

        :param new_current: The new current
        """
        self._assert_valid_current(new_current)
        self._power_supply.lower_sweep_current = new_current

    def sweep_up(self, fast: bool=False) -> None:
        """
        Sweep the current up to the high limit
        :param fast:
        """
        self._power_supply.sweep_up(fast)

    def sweep_down(self, fast: bool=False) -> None:
        """
        Sweep the power supply down to the lower limit

        :param fast: True if the sweep is to be fast
        """
        self._power_supply.sweep_down(fast)

    def sweep_zero(self, fast: bool=False) -> None:
        """
        Sweep the current to zero

        :param fast: True if the sweep is to be fast
        """
        self._power_supply.sweep_zero(fast)

    def pause_sweep(self) -> None:
        """
        Pause sweeping
        """
        self._power_supply.pause_sweep()

    @staticmethod
    def _assert_valid_current(current: Quantity) -> None:
        """

        :param current: The current to check

        """
        if current.units != amperes:
            raise ValueError("The current %s is not in amps", current)
        if float(current) > 100:
            raise ValueError("The current setting is too high")
        if float(current) < -100:
            raise ValueError("The current setting is too low")
