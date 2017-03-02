import abc
from mr_freeze.tasks.abstract_task import AbstractTask


class ReportVariableTask(AbstractTask, metaclass=abc.ABCMeta):
    @abc.abstractproperty
    def title(self) -> str:
        """

        :return: A readable title that will be used as the title
        """
        raise NotImplementedError()
