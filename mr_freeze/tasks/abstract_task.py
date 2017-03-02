"""
Describes an abstract callable task for an executor
"""
import abc
from concurrent.futures import Executor, Future


class AbstractTask(object, metaclass=abc.ABCMeta):
    """
    Describes a task that can be submitted to an executor
    """
    def __call__(self, executor: Executor) -> Future:
        return executor.submit(self.task)

    @abc.abstractmethod
    def task(self):
        """

        The task to execute
        """
        raise NotImplementedError()
