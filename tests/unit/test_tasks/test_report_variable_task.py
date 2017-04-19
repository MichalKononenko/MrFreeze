# coding=utf-8
"""
Contains unit tests for the task that reports variables to the store
"""
import unittest
import unittest.mock as mock
from concurrent.futures import Executor
from mr_freeze.resources.abstract_store import Store
from mr_freeze.tasks.report_variable_task import ReportVariableTask


class TestReportVariableToStoreTask(unittest.TestCase):
    """
    Base class for the unit tests
    """
    def setUp(self):
        self.store = mock.MagicMock(spec=Store)  # type: Store
        self.executor = mock.MagicMock(spec=Executor)  # type: Executor
        self.task = self.ConcreteReportVariableTask(self.store)

    class ConcreteReportVariableTask(ReportVariableTask):
        """
        Contains a concrete definition of what is being reported
        """
        @property
        def variable_type(self):
            """

            :return: The type of variable that is being reported
            """
            return int

        @property
        def variable(self):
            """

            :return: The value of the variable
            """
            return 2


class TestTask(TestReportVariableToStoreTask):
    def test_task(self):
        self.task.task(self.executor)

        self.assertEqual(
            self.task.variable,
            self.store[self.task.variable_type].value
        )
