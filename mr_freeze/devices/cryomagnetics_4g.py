# -*- coding: utf-8 -*-
"""
Implements a Cryomagnetics 4G Power supply for InstrumentKit
"""
from contextlib import contextmanager
from mr_freeze.devices.abstract_cryomagnetics_device \
    import AbstractCryomagneticsDevice
import quantities as pq
from time import sleep
import re
import logging

log = logging.getLogger(__name__)


class Cryomagnetics4G(AbstractCryomagneticsDevice):
    """
    Base class for a Cryomagnetics 4G Superconducting Magnet Power supply
    """
    CHANNELS = {1, 2}

    UNITS = {
        "A": pq.amp,
        "G": pq.gauss
    }

    REVERSE_UNITS = {
        pq.amp: "A",
        pq.gauss: "G"
    }

    MAXIMUM_MESSAGE_SIZE = 1000

    instrument_measurement_timeout = 0.5

    @property
    def terminator(self):
        """

        :return: The termination character for the device. The terminator is
         the carriage return character (ASCII 10), followed by the newline
         character (ASCII 13)
        """
        return '\n'

    @property
    def unit(self):
        """
        The power supply is capable of expressing the output current going
        into the magnet in amperes, but it can also convert the current to a
        predicted magnetic field using a particular relation.

        :return: The units in which the power supply expresses its measurement
        """
        response = self.query("UNITS?")
        return self.UNITS[response]

    @unit.setter
    def unit(self, unit_to_set):
        """
        Set the unit to either amperes or gauss. The valid units to which
        this value can be set are the keys in the ``UNITS`` dictionary of
        this object

        :param str unit_to_set: The unit to set
        :raises: :exc:`ValueError` if the unit cannot be set
        """
        if unit_to_set not in self.UNITS.keys():
            raise ValueError("Attempted to set unit to an invalid value")
        self.query("UNITS %s" % unit_to_set)

    @property
    def current(self):
        """

        :return: The current in amperes being sent out of the power supply
        """
        self.unit = self.REVERSE_UNITS[pq.amp]
        sleep(self.instrument_measurement_timeout)

        return self.parse_current_response(self.query("IOUT?"))

    @property
    def upper_sweep_current(self):
        """

        :return: The sweep current upper limit
        :rtype Quantity
        """
        sleep(self.instrument_measurement_timeout)

        return self.parse_current_response(self.query("ULIM?"))

    @upper_sweep_current.setter
    def upper_sweep_current(self, new_current):
        sleep(self.instrument_measurement_timeout)
        if new_current.units != pq.A:
            raise ValueError("Unable to set current. Units are not amperes")

        with self._requires_remote_mode():
            log.debug("Setting upper sweep current to %f", float(new_current))
            self.query("ULIM %2.4f" % float(new_current))

    @property
    def lower_sweep_current(self):
        """

        :return: The lower limit of the sweep current
        :rtype Quantity
        """
        sleep(self.instrument_measurement_timeout)

        return self.parse_current_response(self.query("LLIM?"))

    @lower_sweep_current.setter
    def lower_sweep_current(self, new_current):
        sleep(self.instrument_measurement_timeout)
        if new_current.units != pq.A:
            raise ValueError("Unable to set current. Units are not amperes")

        with self._requires_remote_mode():
            log.debug("Setting lower sweep current ot %f", float(new_current))
            self.query("LLIM %2.4f" % float(new_current))

    @property
    def persistent_heater_on(self):
        """

        :return: True if the persistent heater is on, and False if not
        """
        return bool(int(self.query("PSHTR?")))

    @property
    def persistent_heater_off(self):
        """

        :return: True if the heater is off and False if it is
        """
        return not self.persistent_heater_on

    def sweep_up(self, fast=False):
        """
        Sweep the current up to the high limit

        :param fast: Set to true if a fast sweep is desired
        """
        log.debug("sweeping to %s", self.upper_sweep_current)

        with self._requires_remote_mode():
            if fast:
                self.query("SWEEP UP FAST")
            else:
                self.query("SWEEP UP")

    def sweep_down(self, fast=False):
        """

        :param fast: Set to true if a fast sweep is desired
        """
        log.debug("sweeping to %s", self.lower_sweep_current)

        with self._requires_remote_mode():
            if fast:
                self.query("SWEEP DOWN FAST")
            else:
                self.query("SWEEP DOWN")

    def sweep_to_zero(self, fast=False):
        """

        :param fast: Set to true if a fast sweep is desired
        """
        log.debug("sweeping to 0")

        with self._requires_remote_mode():
            if fast:
                self.query("SWEEP ZERO FAST")
            else:
                self.query("SWEEP ZERO")

    def pause_sweep(self):
        """

        Pause the sweep
        """
        log.debug("pausing sweep")

        with self._requires_remote_mode():
            self.query("SWEEP PAUSE")

    @staticmethod
    def parse_current_response(response):
        """

        :param str response: The response to parser
        :return: The quantity corresponding to the response
        :rtype: Quantity
        """
        value_match = re.search(r"^(\d|\.|-)*(?=(A|G))", response)
        unit_match = re.search(r".(?=$)", response)

        value = float(value_match.group(0))
        unit = Cryomagnetics4G.UNITS[unit_match.group(0)]

        return_value = value * unit

        log.debug("parsed quantity %s, unit %s from response %s",
                  return_value, unit, response)

        return return_value

    @contextmanager
    def _requires_remote_mode(self):
        """
        For queries that require remote mode in order to operate,
        this method ensures that remote mode is entered, and then local mode is
        returned after the method is complete
        """
        self.query("REMOTE")
        try:
            yield
        finally:
            self.query("LOCAL")
