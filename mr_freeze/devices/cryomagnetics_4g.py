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
        "a": pq.amp,
        "g": pq.gauss
    }

    REVERSE_UNITS = {
        pq.amp: "a",
        pq.gauss: "g"
    }

    MAXIMUM_MESSAGE_SIZE = 1000

    @property
    def terminator(self):
        return '\r\n'

    @property
    def unit(self):
        response = self.query("UNITS?")
        return self.UNITS[response]

    @unit.setter
    def unit(self, unit_to_set):
        if unit_to_set not in self.UNITS.keys():
            raise ValueError("Attempted to set unit to an invalid value")
        self.write("UNITS %s" % unit_to_set)

    @property
    def current(self):
        self.unit = self.REVERSE_UNITS[pq.amp]
        sleep(self.instrument_measurement_timeout)

        return self.parse_current_response(self.query("IOUT?"))

    def query(self, cmd, size=-1):
        self._querying_lock.acquire()
        self.write(cmd + self.terminator)

        response = self.read(size=self.MAXIMUM_MESSAGE_SIZE)
        log.debug("received response %s", response)
        self._querying_lock.release()

        return self.parse_query(cmd, response)

    @staticmethod
    def parse_current_response(response):
        value_match = re.search("^(\d|\.)*(?=\s)", response)
        unit_match = re.search("(?<=\s).*(?=$)", response)

        value = float(value_match.group(0))
        unit = Cryomagnetics4G.UNITS[unit_match.group(0)]

        return_value = value * unit

        log.debug("parsed quantity %s from response %s", return_value, unit)

        return return_value

    @staticmethod
    def parse_query(command, response):
        log.debug("Query parser received command %s and response %s",
                  command, response)

        echoed_command = re.search("^.*(?=\r\r\n)", response)
        response_from_device = re.search(
            "(?<=\r\r\n).*(?=\r\n$)",
            response
        )

        log.debug(
            "Query parser parsed echoed command %s and response %s",
            echoed_command, response_from_device
        )

        if (echoed_command is None) or (response_from_device is None):
            raise RuntimeError(
                "Cryomagnetics query parser did not match search string"
            )

        if command != echoed_command.group(0):
            raise RuntimeError(
                "Cryomagnetics query parser did not find echoed command"
            )

        if response_from_device.group(0) is None:
            raise RuntimeError(
                "I/O with Cryomagnetics instrument did not return a response"
            )

        return response_from_device.group(0)
