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
        return '\r\n'

    @property
    def unit(self):
        response = self.query("UNITS?")
        return self.UNITS[response]

    @unit.setter
    def unit(self, unit_to_set):
        if unit_to_set not in self.UNITS.keys():
            raise ValueError("Attempted to set unit to an invalid value")
        self.query("UNITS %s" % unit_to_set)

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
        value_match = re.search("^(\d|\.)*(?=(A|G))", response)
        unit_match = re.search(".(?=$)", response)

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

        if echoed_command is None:
            raise RuntimeError(
                "Cryomagnetics query parser did not match search string"
            )

        if response_from_device is None:
            response = ''
        else:
            response = response_from_device.group(0)

        if command != echoed_command.group(0):
            raise RuntimeError(
                "Cryomagnetics query parser did not find echoed command"
            )

        log.debug(
            "Query parser parsed echoed command %s and response %s",
            echoed_command.group(0), response
        )

        return response
