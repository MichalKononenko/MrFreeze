from concurrent.futures import Executor
from mr_freeze.tasks.abstract_task import AbstractTask
from mr_freeze.resources.csv_file import CSVFile


class WriteCSVTitle(AbstractTask):
    file_timeout_in_seconds = 1

    def __init__(self, csv_file: CSVFile):
        self.file = csv_file

    def task(self, executor: Executor):
        self.file.write_titles()
