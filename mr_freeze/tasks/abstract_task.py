# -*- coding: utf-8
"""
Describes an abstract callable task for an executor
"""
import abc
import logging
from typing import Any, Optional
from concurrent.futures import Executor, Future

log = logging.getLogger(__name__)


class AbstractTask(object, metaclass=abc.ABCMeta):
    """
    Describes a task that can be submitted to an executor
    """
    def __call__(self, executor: Executor) -> Future:
        log.debug("Submitted task <%s> to executor <%s>", self.__repr__(),
                  executor.__repr__())

        return executor.submit(self.task, executor)

    @abc.abstractmethod
    def task(self, executor: Executor) -> Optional[Any]:
        """

        The task to execute
        """
        raise NotImplementedError()

    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)
