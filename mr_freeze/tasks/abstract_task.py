# -*- coding: utf-8
"""
Describes an abstract callable task for an executor
"""
import abc
import logging
from typing import Any, Optional, Callable
from functools import wraps
from concurrent.futures import Executor, Future

log = logging.getLogger(__name__)


class AbstractTask(object, metaclass=abc.ABCMeta):
    """
    Describes a task that can be submitted to an executor
    """
    def __call__(self, executor: Executor) -> Future:
        log.debug("Submitted task <%s> to executor <%s>", self.__repr__(),
                  executor.__repr__())

        return executor.submit(self._task_wrapper(self.task), executor)

    @abc.abstractmethod
    def task(self, executor: Executor) -> Optional[Any]:
        """

        The task to execute
        """
        raise NotImplementedError()

    def _task_wrapper(
            self, task: Callable[['AbstractTask', Executor], Optional[Any]]
    ) -> Callable[[Executor], Optional[Any]]:
        """
        Wraps the method to be executed, adding in some logging should the
        task fail

        :param task: The task function to wrap
        :return: The wrapped function
        """
        @wraps(task)
        def wrapper(*args, **kwargs) -> Optional[Any]:
            """

            :param args: The arguments to the original task function
            :param kwargs: The keyword arguments to the original task function
            :return: The return value of the task
            """
            try:
                return task(*args, **kwargs)
            except BaseException as error:
                log.error(
                    "Task %s threw error %s", repr(self), repr(error)
                )
                raise error
        return wrapper

    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)
