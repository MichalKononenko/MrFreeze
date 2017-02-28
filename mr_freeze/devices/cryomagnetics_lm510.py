"""
Contains an implementation of the cryomagnetics LM 510 liquid cryogen level
monitor
"""
from threading import Lock
from instruments.abstract_instruments import Instrument as _Instrument
import quantities as pq
import re
from time import sleep


class CryomagneticsLM510(_Instrument):
    """
    Represents a Cryomagnetics LM-510 liquid cryogen level monitor
    """
    CHANNELS = {1, 2}

    channel_measurement_lock = Lock()  # type: Lock

    measurement_timeout = 1

    UNITS = {
        "CM": pq.cm,
        "IN": pq.inch,
        "%": pq.percent,
        "PERCENT": pq.percent
    }

    @property
    def channel(self):
        return int(self.query("CHAN?"))

    @channel.setter
    def channel(self, channel):
        if channel not in self.CHANNELS:
            raise ValueError("Attempted to set channel to %s. Channel must "
                             "be an integer of either 1 or 2", channel)
        command = "CHAN %d" % channel
        self.query(command)

    @property
    def status_byte(self):
        byte_as_string = self.query("*STB?")
        return bytes([int(byte_as_string)])

    @property
    def channel_1_data_ready(self):
        status_byte = self.status_byte
        return bool(status_byte[0] % 1)

    @property
    def channel_2_data_ready(self):
        status_byte = self.status_byte
        return bool(status_byte[0] % 4)

    @property
    def channel_1_measurement(self, measurer=None):
        return self._measurement(1, measurer)

    @property
    def channel_2_measurement(self, measurer=None):
        return self._measurement(2, measurer)

    def _measurement(self, channel_number, measurer=None):
        if measurer is None:
            measurer = self._ChannelMeasurement(channel_number, self)

        response = measurer.measurement

        return self.parse_response(response)

    @staticmethod
    def parse_response(response):
        value_match = re.search("^(\d|\.)*(?=\s)", response)
        unit_match = re.search("(?<=\s).*(?=$)", response)

        value = float(value_match.group(0))
        unit = CryomagneticsLM510.UNITS[unit_match.group(0)]

        return value * unit

    class _ChannelMeasurement(object):
        """
        Prepares a measurement of a channel, and returns a string stating
        what the measurement was.
        """

        def __init__(
                self, channel_number, instrument
        ):
            """

            :param int channel_number: The number of the channel to measure.
                Must be 1 or 2
            :param Instrument instrument: the managed instrument
            """
            self.channel = channel_number
            self.instrument = instrument

        @property
        def measurement(self):
            """

            :return: The string returned from the level measurement
            """
            self.instrument.channel_measurement_lock.acquire()
            self.instrument.query("MEAS %d", self.channel)
            sleep(self.instrument.measurement_timeout)

            response = self.instrument.query("MEAS? %d", self.channel)

            return response
