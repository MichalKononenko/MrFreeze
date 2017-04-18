# coding=utf-8
"""
Describes how to report a variable to the store
"""
import abc
import logging
from concurrent.futures import Executor
from mr_freeze.tasks.abstract_task import AbstractTask
from mr_freeze.resources.abstract_store import Variable, V, Store
from six import add_metaclass

log = logging.getLogger(__name__)


@add_metaclass(abc.ABCMeta)
class ReportVariableTask(AbstractTask):
    """
    Write a task to the store
    """
    def __init__(self, store: Store):
        """

        :param store: The store to which the new value of the variable is to be
         reported
        """
        super(ReportVariableTask, self).__init__()
        self.store = store

    def task(self, executor: Executor) -> None:
        """

        Get the new value and write it to the store

        :param executor: The executor to use for the task
        """
        self.store[self.variable_type].value = self.variable

    @abc.abstractproperty
    def variable_type(self) -> Variable.__class__:
        """

        :return: The type of variable that this task reports
        """
        return Variable

    @abc.abstractproperty
    def variable(self) -> V:
        """

        :return: The new value of the variable
        """
        raise NotImplementedError()

    def __repr__(self) -> str:
        return "{0}(store={1})".format(self.__class__.__name__, self.store)
