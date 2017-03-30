# coding=utf-8
"""
Describes a task to write the required measurements to a pipe
"""
from concurrent.futures import Executor
from typing import Iterable, Tuple
from mr_freeze.tasks.abstract_task import AbstractTask
from mr_freeze.tasks.report_variable_task import ReportVariableTask
from mr_freeze.resources.measurement_pipe import Pipe


class WriteToPipe(AbstractTask):
    """
    Describes a task to write data as a JSON file
    """
    def __init__(
            self, pipe: Pipe, variables: Iterable[
                Tuple[ReportVariableTask, float]
            ]
    ) -> None:
        self.pipe = pipe
        self.variables = variables

    def task(self, executor: Executor) -> None:
        """

        :param executor: The executor to be used for running the task
        """
        data = {var[0].title: var[1] for var in self.variables}
        self.pipe.data = data
        self.pipe.flush()

    def __repr__(self):
        return '%s(pipe=%s, variables=%s)' % (
            self.__class__.__name__, self.pipe, self.variables
        )
