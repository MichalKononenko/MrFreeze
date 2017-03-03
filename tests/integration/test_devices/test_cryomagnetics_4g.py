import logging
import sys
import unittest
from mr_freeze.devices.cryomagnetics_4g import Cryomagnetics4G
from mr_freeze.devices.cryomagnetics_4g import log as device_log
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
device_log.setLevel(logging.DEBUG)
device_log.addHandler(ch)

TESTING_PARAMETERS = {
    "instrument-port": "/dev/ttyUSB1",
    "baud-rate": 9600,
    "reset-command": "*RST",
    "timeout": 2
}


class TestCryomagnetics4G(unittest.TestCase):

    def setUp(self):
        self.instrument = Cryomagnetics4G.open_serial(
            port=TESTING_PARAMETERS["instrument-port"],
            baud=TESTING_PARAMETERS["baud-rate"],
            write_timeout=TESTING_PARAMETERS["timeout"],
            timeout=TESTING_PARAMETERS["timeout"]
        )
        log.info("Started integration test %s with parameters %s",
                 self, TESTING_PARAMETERS)

    def test_can_connect(self):
        response = self.instrument.query("*IDN?")
        self.assertIsInstance(response, str)
        self.assertNotEqual(response, "*IDN?")


class TestCurrent(TestCryomagnetics4G):
    def test_current(self):
        self.assertIsInstance(
            self.instrument.current, Quantity
        )


class TestAtomicity(TestCryomagnetics4G):
    def test_atomicity(self):
        response1 = self.instrument.query("*IDN?")
        response2 = self.instrument.current
        self.assertNotEqual(response1, response2)
