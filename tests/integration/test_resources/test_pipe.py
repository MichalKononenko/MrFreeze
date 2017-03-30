# coding=utf-8
"""
Contains integration tests for the measurement pipe
"""
import unittest
import os
import json
import gc
import quantities as pq
from mr_freeze.resources.measurement_pipe import Pipe

TEST_PARAMETERS = {
    "location": os.path.join(os.path.curdir, 'pipe-test.json'),
    "pre-populated_test_data": {
        "foo": "bar",
        "baz": "luhrmann",
        "unit": 4.0 * pq.A
    }
}


class TestPipe(unittest.TestCase):
    def setUp(self):
        self.location = TEST_PARAMETERS["location"]
        self.test_data = TEST_PARAMETERS["pre-populated_test_data"]
        self.pipe = Pipe(self.location)

    def tearDown(self):
        if os.path.isfile(self.location):
            os.remove(self.location)


class TestFromFile(TestPipe):
    def setUp(self):
        TestPipe.setUp(self)

        with open(self.location, mode='w') as f:
            json.dump(self.test_data, f)

    def test_from_file(self):
        pipe = Pipe.from_file(self.location)

        self.assertEqual(
            self.test_data, pipe.data
        )


class TestFlush(TestPipe):
    def test_flush(self):
        self.pipe.data = self.test_data
        self.pipe.flush()

        del self.pipe
        gc.collect()

        pipe = Pipe.from_file(self.location)
        self.assertEqual(
            self.test_data, pipe.data
        )
