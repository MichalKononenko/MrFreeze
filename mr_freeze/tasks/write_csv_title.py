"""
Describes a task for writing the title row into a CSV file.
"""
from concurrent.futures import Executor
from mr_freeze.tasks.abstract_task import AbstractTask
from mr_freeze.resources.csv_file import CSVFile


class WriteCSVTitle(AbstractTask):
    """
    The task for writing titles to the CSV files
    """
    file_timeout_in_seconds = 1

    def __init__(self, csv_file: CSVFile) -> None:
        """

        :param csv_file: The CSV file to which titles will be written
        """
        self.file = csv_file

    def task(self, executor: Executor) -> None:
        """
        Write the required titles

        :param executor: The executor to use for performing the task
        """
        self.file.write_titles()
