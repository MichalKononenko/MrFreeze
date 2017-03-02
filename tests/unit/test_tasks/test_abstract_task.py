import unittest
import unittest.mock as mock
from concurrent.futures import Executor
from mr_freeze.tasks.abstract_task import AbstractTask


class ConcreteTask(AbstractTask):
    """
    Describes a task that only returns 1
    """
    def task(self, executor: Executor) -> int:
        """

        :return: The number ``1``
        """
        return 1


class TestAbstractTask(unittest.TestCase):
    """
    Contains unit tests for
    :class:`mr_freeze.tasks.abstract_task.AbstractTask`
    """
    executor = mock.MagicMock(spec=Executor)

    def setUp(self):
        """
        Instantiate a concrete task
        """
        self.task = ConcreteTask()


class TestCall(TestAbstractTask):
    """
    Tests that calling the task with an executor successfully submits the task
    """

    def test_submit(self):
        """
        Tests that the callable task was successfully submitted to the
        executor
        """
        self.task(self.executor)

        self.assertTrue(self.executor.submit.called)
        self.assertEqual(
            mock.call(self.task.task, self.executor),
            self.executor.submit.call_args
        )
