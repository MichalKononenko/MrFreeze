import logging
import sys
import unittest
from mr_freeze.devices.cryomagnetics_4g import Cryomagnetics4G
from quantities import Quantity, amperes

log = logging.getLogger()
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
ch.setFormatter(formatter)

TESTING_PARAMETERS = {
    "instrument-port": "/dev/ttyUSB0",
    "baud-rate": 9600,
    "reset-command": "*RST",
    "timeout": 1,
    "current-to-set": 0.01 * amperes
}


class TestCryomagnetics4G(unittest.TestCase):

    def setUp(self):
        self.instrument = Cryomagnetics4G.open_serial(
            port=TESTING_PARAMETERS["instrument-port"],
            baud=TESTING_PARAMETERS["baud-rate"],
            write_timeout=TESTING_PARAMETERS["timeout"],
            timeout=TESTING_PARAMETERS["timeout"]
        )
        log.addHandler(ch)
        log.info("Started integration test %s with parameters %s",
                 self, TESTING_PARAMETERS)

    def test_can_connect(self):
        response = self.instrument.query("*IDN?")
        self.assertIsInstance(response, str)
        self.assertNotEqual(response, "*IDN?")

    def tearDown(self):
        log.removeHandler(ch)


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


class TestUpperSweepCurrent(TestCryomagnetics4G):
    def setUp(self):
        TestCryomagnetics4G.setUp(self)
        self.starting_current = self.instrument.upper_sweep_current

    def tearDown(self):
        self.instrument.upper_sweep_current = self.starting_current
        TestCryomagnetics4G.tearDown(self)

    def test_getter(self):
        self.assertIsInstance(
            self.instrument.upper_sweep_current, Quantity
        )

    def test_setter(self):
        self.instrument.upper_sweep_current = \
            TESTING_PARAMETERS["current-to-set"]

        self.assertAlmostEqual(
            float(TESTING_PARAMETERS["current-to-set"]),
            float(self.instrument.upper_sweep_current),
            delta=1e-2
        )


class TestLowerSweepCurrent(TestCryomagnetics4G):
    def setUp(self):
        TestCryomagnetics4G.setUp(self)
        self.starting_current = self.instrument.lower_sweep_current

    def tearDown(self):
        self.instrument.lower_sweep_current = self.starting_current
        TestCryomagnetics4G.tearDown(self)

    def test_getter(self):
        self.assertIsInstance(
            self.instrument.lower_sweep_current, Quantity
        )

    def test_setter(self):
        self.instrument.lower_sweep_current = TESTING_PARAMETERS[
            "current-to-set"]
        self.assertAlmostEqual(
            float(TESTING_PARAMETERS["current-to-set"]),
            float(self.instrument.upper_sweep_current),
            delta=1e-2
        )


class TestSweepUp(TestCryomagnetics4G):
    """
    Tests that the sweep to the high limit works correctly
    """
    def setUp(self):
        TestCryomagnetics4G.setUp(self)
        self.initial_current = self.instrument.upper_sweep_current
        self.instrument.upper_sweep_current = TESTING_PARAMETERS["current-to-set"]

    def tearDown(self):
        self.instrument.upper_sweep_current = self.initial_current
        self.instrument.sweep_to_zero()
        TestCryomagnetics4G.tearDown(self)

    def test_sweep_up(self):
        self.instrument.sweep_up()
        self.assertAlmostEqual(
            TESTING_PARAMETERS["current-to-set"], self.instrument.current,
            delta=1e-3
        )

    def test_sweep_up_then_to_low_value(self):
        self.instrument.upper_sweep_current = 0.25 * amperes
        self.instrument.sweep_up()
        self.instrument.upper_sweep_current = 0.1 * amperes
        self.instrument.sweep_up()
        self.assertAlmostEqual(
            0.1, float(self.instrument.current),
            delta=1e-1
        )
