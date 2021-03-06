# -*- coding: utf-8 -*-
"""
Contains an adapter for working with the Cryomagnetics LM 510. This object
provides a layer of abstraction between the InstrumentKit implementation of
the device, and a working device
"""
import logging
from typing import Optional, List
from numpy import nan
from quantities import Quantity, cm
from instruments.abstract_instruments import Instrument as _Instrument
from mr_freeze.exceptions import DeviceCommunicationError
from mr_freeze.devices.cryomagnetics_lm510 import CryomagneticsLM510 as \
    _CryomagneticsLM510

log = logging.getLogger(__name__)


class CryomagneticsLM510(object):
    """
    Adapter layer for the Cryomagnetics LM 510 level meter
    """
    _port = '/dev/ttyUSB0'  # type: str
    _baud_rate = 9600  # type: int
    _timeout_in_seconds = 3.0  # type: float
    _managed_instance = None  # type: _Instrument
    _constructor = _CryomagneticsLM510  # type: _Instrument

    null_value = nan * cm

    INDEX_TO_INSTRUMENT_CHANNELS = \
        _CryomagneticsLM510.INDEX_TO_INSTRUMENT_CHANNELS

    ALLOWED_CHANNELS = INDEX_TO_INSTRUMENT_CHANNELS.values()

    @property
    def port_name(self) -> str:
        """

        :return: The name of the port to which this device is attached
        """
        return self._port

    @port_name.setter
    def port_name(self, new_port_name: str):
        """

        :param str new_port_name: The desired port name for the device
        """
        self._port = new_port_name

    @property
    def baud_rate(self) -> int:
        """

        :return: The instrument baud rate
        :rtype: int
        """
        return self._baud_rate

    @baud_rate.setter
    def baud_rate(self, new_baud_rate: int):
        """

        :param int new_baud_rate: The desired baud rate
        """
        self._baud_rate = new_baud_rate

    @property
    def timeout_in_seconds(self) -> float:
        """

        :return: The elapsed time for which the instrument will wait for a
            response. After this, it will be assumed that the device has not
            provided a response, and an :exc:`IOError` will be raised.
        :rtype: float
        """
        return self._timeout_in_seconds

    @timeout_in_seconds.setter
    def timeout_in_seconds(self, new_timeout: float):
        """

        :param float new_timeout: The desired message timeout
        """
        self._timeout_in_seconds = new_timeout

    @property
    def _level_meter(self) -> Optional[_CryomagneticsLM510]:
        """

        :return: An instance of the level meter with the desired parameters
        """
        if self._managed_instance is None:
            self._managed_instance = self._constructor.open_serial(
                port=self.port_name, baud=self.baud_rate
            )
        return self._managed_instance

    @property
    def channel_1_measurement(self) -> Quantity:
        """

        :return: A measurement on Channel 1 of the device
        """
        return self._measurement(0)

    @property
    def channel_2_measurement(self) -> Quantity:
        """

        :return: A measurement on Channel 2 of the device
        """
        return self._measurement(1)

    def _measurement(self, channel_number) -> Quantity:
        """

        :param int channel_number: The channel on which to measure
        :return:
        """
        channel = self._level_meter[channel_number]

        try:
            value = channel.measurement
        except DeviceCommunicationError as error:
            log.error(
                "Trying to measure channel %s threw %s",
                channel_number, error
            )
            value = self.null_value

        return value if value is not None else self.null_value
