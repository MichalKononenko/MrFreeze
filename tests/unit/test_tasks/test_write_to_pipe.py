# coding=utf-8
"""
Contains unit tests for :mod:`mr_freeze.tasks.write_to_pipe`
"""
import unittest
import unittest.mock as mock
import os
from concurrent.futures import Executor
from mr_freeze.resources.measurement_pipe import Pipe
from mr_freeze.tasks.report_liquid_helium_level import ReportLiquidHeliumLevel
from mr_freeze.tasks.write_to_pipe import WriteToPipe


class TestWriteToPipe(unittest.TestCase):

    def setUp(self):
        self.location = os.devnull
        self.variables = ((ReportLiquidHeliumLevel, 3.0),)
        self.pipe = mock.MagicMock(spec=Pipe)  # type: Pipe
        self.executor = mock.MagicMock(spec=Executor)  # type: Executor

        self.task = WriteToPipe(self.pipe, self.variables)

    def test_task(self):
        with mock.patch('mr_freeze.tasks.write_to_pipe.Pipe.from_file',
                        return_value=self.pipe) as mock_pipe:
            self.task.task(self.executor)

        self.assertTrue(self.pipe.flush.called)
        self.assertIsInstance(self.pipe.data, dict)
        self.assertEqual({ReportLiquidHeliumLevel.title: 3.0}, self.pipe.data)
