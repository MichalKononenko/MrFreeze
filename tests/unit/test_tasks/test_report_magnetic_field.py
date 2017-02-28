"""
Contains unit tests for :mod:`mr_freeze.tasks.report_magnetic_field`
"""
import unittest
import unittest.mock as mock
from concurrent.futures import Executor
from mr_freeze.devices.lakeshore_475 import Lakeshore475
from mr_freeze.tasks.report_magnetic_field import ReportMagneticField


class TestReportMagneticField(unittest.TestCase):
    """
    Base class for unit tests of
    :class:`mr_freeze.tasks.report_magnetic_field.ReportMagneticField`
    """
    gauge = mock.MagicMock(spec=Lakeshore475)  # type: Lakeshore475
    executor = mock.MagicMock(spec=Executor)  # type: Executor

    def setUp(self):
        """
        Initialize the task fixture
        """
        self.task = ReportMagneticField(gauge=self.gauge)


class TestInitializer(TestReportMagneticField):
    """
    Contains unit tests for the initializer
    """
    def test_field(self):
        """
         Assert that the correct gauge was instantiated
        """
        self.assertEqual(self.gauge, self.task.gauge)


class TestCall(TestReportMagneticField):
    """
    Contains tests to evaluate what happens when the task is called
    """
    def test_call(self):
        """
        Tests that calling the task with an executor results in the task
        being submitted to the executor
        """
        self.task(self.executor)
        self.assertTrue(
            self.executor.submit.called
        )
        self.assertTrue(hasattr(self._task_function, '__call__'))

    def test_run_task(self):
        """
        Tests that the task runs correctly
        """
        self.task(self.executor)
        field_strength = self._task_function()
        self.assertEqual(self.gauge.magnetometer.field, field_strength)

    @property
    def _task_function(self):
        """

        :return: The function with which the submit method to the executor
        was called
        """
        return self.executor.submit.call_args[0][0]
