import unittest
import quantities as pq
from mr_freeze.devices.cryomagnetics_4g import Cryomagnetics4G


class TestCryomagnetics4G(unittest.TestCase):
    pass


class TestParseQuery(TestCryomagnetics4G):
    test_parameters = (
        ("87.424A", 87.424 * pq.amps),
        ("3240G", 3240 * pq.gauss)
    )

    def test_parser(self):
        for parameter in self.test_parameters:
            self._run_test(parameter)

    def _run_test(self, parameter: tuple):
        self.assertEqual(
            parameter[1],
            Cryomagnetics4G.parse_current_response(parameter[0])
        )
