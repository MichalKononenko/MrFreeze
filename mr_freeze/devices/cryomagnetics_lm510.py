"""
Contains an implementation of the cryomagnetics LM 510 liquid cryogen level
monitor
"""
from threading import Lock
from mr_freeze.devices.abstract_cryomagnetics_device \
    import AbstractCryomagneticsDevice
import quantities as pq
import re
import logging
from time import sleep

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class CryomagneticsLM510(AbstractCryomagneticsDevice):
    """
    Represents a Cryomagnetics LM-510 liquid cryogen level monitor
    """
    CHANNELS = {1, 2}

    channel_measurement_lock = Lock()  # type: Lock
    querying_lock = Lock()  # type: Lock

    measurement_timeout = 1

    UNITS = {
        "cm": pq.cm,
        "in": pq.inch,
        "%": pq.percent,
        "percent": pq.percent
    }

    @property
    def default_channel(self):
        return int(self.query("CHAN?"))

    @default_channel.setter
    def default_channel(self, channel):
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

    def reset(self):
        self.query("*RST")

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

        return_value = value * unit

        log.debug("parsed quantity %s from response %s", return_value,
                  response)
        return return_value

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
            sleep(self.instrument.measurement_timeout)

            response = self.instrument.query("MEAS? %d" % self.channel)

            self.instrument.channel_measurement_lock.release()
            return response
