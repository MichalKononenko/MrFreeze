# coding=utf-8
"""
Contains unit tests for the csv logger
"""
import unittest
import unittest.mock as mock
import os
import csv
from concurrent.futures import Executor
from mr_freeze.resources.application_state import Store, LoggingInterval
from mr_freeze.resources.csv_file import CSVLogger


class TestCSVLogger(unittest.TestCase):
    def setUp(self):
        self.file_path = os.path.join(os.curdir, 'file.csv')
        self.executor = mock.MagicMock(spec=Executor)  # type: Executor
        self.store = Store(self.executor)
        self.scheduler = mock.MagicMock()
        self.logger = CSVLogger(
            self.store, self.file_path, self.executor
        )

    def tearDown(self):
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)


class TestStartLogging(TestCSVLogger):
    def test_start_logging(self):
        self.logger.start_logging(self.scheduler)
        self.assertTrue(
            self.scheduler.every(self.store[LoggingInterval].value).minutes.do(
                self.logger.write_values
            ).tag.called
        )


class TestStopLogging(TestCSVLogger):
    def test_stop_logging(self):
        self.logger.stop_logging(self.scheduler)
        self.assertTrue(
            self.scheduler.clear.called
        )


class TestWriteTitles(TestCSVLogger):
    """
    Tests that titles are successfully written
    """
    def test_write_titles(self):
        self.logger.write_titles()

        with open(self.file_path) as file:
            reader = csv.DictReader(file)
            names = reader.fieldnames

        self.assertEqual(
            set(names), set(self.logger.VARIABLE_TITLES.values())
        )


class TestWriteValues(TestCSVLogger):
    """
    Tests that values are successfully written to the CSV file
    """
    def test_write_values(self):
        self.logger.write_titles()
        self.logger.write_values()

        self.assertTrue(os.path.isfile(self.file_path))
