import unittest
import logging
import sys
from quantities import Quantity
from mr_freeze.devices.lakeshore_475 import Lakeshore475

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
ch.setFormatter(formatter)
log.addHandler(ch)

TESTING_PARAMETERS = {
    "port": "/dev/ttyUSB0",
    "address": 12
}


class TestLakeshore475(unittest.TestCase):
    def setUp(self):
        self.meter = Lakeshore475()
        self.meter.port_name = TESTING_PARAMETERS["port"]
        self.meter.address = TESTING_PARAMETERS["address"]

    def test_field(self):
        self.assertIsInstance(
            self.meter.field, Quantity
        )


class TestNDACBug(TestLakeshore475):
    def test_ndac_bug(self):
        field1 = self.meter._magnetometer.query("*IDN?")
        field2 = self.meter.field

        self.assertIsInstance(
            field1, str
        )
        self.assertIsInstance(
            field2, Quantity
        )
