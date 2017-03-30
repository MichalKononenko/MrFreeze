# coding=utf-8
"""
Contains tests for :mod:`mr_freeze.main_loop`
"""
import unittest
import unittest.mock as mock
import os
from mr_freeze.main_loop import MainLoop
from threading import Thread
from time import sleep


class TestMainLoop(unittest.TestCase):
    """
    Contains unit tests for the main loop. Initialize all directories to
    ``/dev/null``.
    """
    loop_timeout = 4

    def setUp(self):
        self.csv_file_path = os.devnull
        self.pipe_file_path = os.devnull
        self.ln2_gauge_port = os.devnull
        self.magnetometer_port = os.devnull
        self.power_supply_port = os.devnull
        self.time_between_reports = 10
        self.task_timeout = 10

        self.loop = MainLoop(
            self.csv_file_path, self.pipe_file_path, self.ln2_gauge_port,
            self.magnetometer_port, self.power_supply_port,
            self.time_between_reports, self.task_timeout
        )

    class LoopTimeoutThread(Thread):
        """
        Stop the loop after a timeout has been reached
        """
        def __init__(self, loop: MainLoop, timeout: int, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.loop = loop
            self.timeout = timeout

        def run(self, *args, **kwargs) -> None:
            """
            Wait for a timeout, then kill the loop.

            :param args:
            :param kwargs:
            :return:
            """
            sleep(self.timeout - 2)
            self.loop.interrupt()

        def __enter__(self):
            self.start()

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.join(self.timeout)


class TestInterrupt(TestMainLoop):
    def test_interrupt(self):
        self.assertTrue(self.loop.should_run)
        self.loop.interrupt()
        self.assertFalse(self.loop.should_run)


class TestRun(TestMainLoop):
    def setUp(self):
        TestMainLoop.setUp(self)
        self.loop._write_title = mock.MagicMock()
        self.loop._run_loop = mock.MagicMock()

    def test_run(self):
        with self.LoopTimeoutThread(self.loop, self.loop_timeout):
            self.loop.run()

        self.assertTrue(self.loop._write_title.called)
        self.assertTrue(self.loop._run_loop.called)
