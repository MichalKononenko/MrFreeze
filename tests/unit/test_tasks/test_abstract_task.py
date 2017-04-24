import unittest
import unittest.mock as mock
from concurrent.futures import Executor, ThreadPoolExecutor
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


class TestCallWithRealExecutor(TestAbstractTask):
    def setUp(self):
        TestAbstractTask.setUp(self)
        self.executor = ThreadPoolExecutor(max_workers=1)

    def test_submit(self):
        result = self.task(self.executor).result()
        self.assertEqual(result, 1)

    @mock.patch("mr_freeze.tasks.abstract_task.log.error")
    def test_submit_exception_is_thrown(self, mock_error):
        """
        Tests that an exception is re-thrown in the executor.

        :param mock_error: A mock call to the function that logs errors.
        """
        bad_task = self.ConcreteFaultyTask()

        with self.assertRaises(ValueError):
            bad_task(self.executor).result()

        self.assertTrue(mock_error.called)

    class ConcreteFaultyTask(AbstractTask):
        """
        Task that throws an exception
        """
        def task(self, executor: Executor) -> None:
            """
            Throw an exception

            :param executor: The executor
            """
            raise ValueError("Kaboom")