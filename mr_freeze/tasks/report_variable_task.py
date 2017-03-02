import abc
from mr_freeze.tasks.abstract_task import AbstractTask


class ReportVariableTask(AbstractTask, metaclass=abc.ABCMeta):
    title = "Abstract Task"
