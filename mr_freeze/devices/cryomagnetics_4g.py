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

    @staticmethod
    def parse_current_response(response):
        value_match = re.search("^(\d|\.)*(?=\s)", response)
        unit_match = re.search("(?<=\s).*(?=$)", response)

        value = float(value_match.group(0))
        unit = Cryomagnetics4G.UNITS[unit_match.group(0)]

        return_value = value * unit

        log.debug("parsed quantity %s from response %s", return_value, unit)

        return return_value