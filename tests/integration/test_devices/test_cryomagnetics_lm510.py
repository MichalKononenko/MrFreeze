"""
Contains integration tests for the cryogen measuring unit

.. note::
    This suite contains a set of testing parameters in the dictionary
    ``TESTING_PARAMETERS``. These parameters must be set to their correct
    values before running the integration test
"""
import unittest
import logging
import sys
from mr_freeze.devices.cryomagnetics_lm510 import CryomagneticsLM510
from mr_freeze.devices.cryomagnetics_lm510 import log as device_log
from quantities import Quantity

log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
ch.setFormatter(formatter)
log.addHandler(ch)
device_log.addHandler(ch)

TESTING_PARAMETERS = {
    "instrument-port": "/dev/ttyUSB1",
    "baud-rate": 9600,
    "gpib-address": 1,
    "channel-to-measure": 2,
    "timeout": 5
}


class TestCryomagneticsLM510(unittest.TestCase):
    def setUp(self):
        self.instrument = CryomagneticsLM510.open_serial(
            port=TESTING_PARAMETERS["instrument-port"],
            baud=TESTING_PARAMETERS["baud-rate"],
            write_timeout=TESTING_PARAMETERS["timeout"],
            timeout=TESTING_PARAMETERS["timeout"]
        )
        log.info(
            "Started integration test %s with parameters %s",
            self, TESTING_PARAMETERS
        )

    def test_can_connect(self):
        response = self.instrument.query("*IDN?")
        self.assertIsInstance(response, str)
        self.assertNotEqual(response, "*IDN?")


class TestChannel1DataReady(TestCryomagneticsLM510):
    def test_channel_1_data_ready(self):
        log.info("Received value of %s from channel 1 data ready method",
                 self.instrument.channel_1_data_ready)
        self.assertIsInstance(
            self.instrument.channel_1_data_ready, bool
        )


class TestChannel2DataReady(TestCryomagneticsLM510):
    def test_channel_2_data_ready(self):
        log.info("Received value of %s from channel 2 data ready method",
                 self.instrument.channel_2_data_ready)
        self.assertIsInstance(
            self.instrument.channel_2_data_ready, bool
        )


class TestMeasurement(TestCryomagneticsLM510):
    def test_channel_to_measure(self):
        if TESTING_PARAMETERS["channel-to-measure"] == 1:
            self._test_channel_1()
        elif TESTING_PARAMETERS["channel-to-measure"] == 2:
            self._test_channel_2()

    def _test_channel_1(self):
        log.info(
            "Received value of %s from meter channel 1",
            self.instrument.channel_1_measurement
        )
        self.assertIsInstance(self.instrument.channel_1_measurement, Quantity)

    def _test_channel_2(self):
        log.info(
            "Received value of %s from meter channel 2",
            self.instrument.channel_2_measurement
        )
        self.assertIsInstance(self.instrument.channel_2_measurement, Quantity)
