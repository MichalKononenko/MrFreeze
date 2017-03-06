"""
Contains a task that can write a set of measured variables to the CSV file
"""
from typing import Iterable
from concurrent.futures import Executor
from mr_freeze.tasks.abstract_task import AbstractTask
from mr_freeze.resources.csv_file import CSVFile


class WriteCSVValues(AbstractTask):
    """
    Describes how to write values to the CSV file
    """
    def __init__(self, file: CSVFile, values_to_write: Iterable) -> None:
        """

        :param file: The file resource to which the values will be written
        :param values_to_write: The values that are to be written to the CSV
            file
        """
        self.values = values_to_write
        self.file = file

    def task(self, executor: Executor) -> None:
        """
        Write the required values

        :param executor: The executor with which this task is to be executed
        """
        self.file.write_values(self.values)
