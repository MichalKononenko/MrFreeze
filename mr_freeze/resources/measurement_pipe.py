# coding=utf-8
"""
Describes a pipe that can be used to write the last sample live
"""
import json
import logging
from quantities import Quantity

log = logging.getLogger(__name__)


class Pipe(object):
    """
    Describes a FIFO pipe of samples that are to be written to the device
    """
    def __init__(self, location: str) -> None:
        self.location = location
        self._data = {}

    @property
    def data(self) -> dict:
        """

        :return: The current data
        """
        return self._data

    @data.setter
    def data(self, new_data: dict) -> None:
        processed_data = self._make_quantities_serializable(new_data)
        self._data = processed_data
        log.debug(
            "Wrote data %s to buffer of pipe %s", new_data, self.__repr__()
        )

    @classmethod
    def from_file(cls, file: str):
        """

        :param file: The file from which the class is to be made
        :return:
        """
        pipe = cls(file)
        pipe.populate_data_from_file(file)
        return pipe

    def populate_data_from_file(self, file: str) -> None:
        """

        :param file: The file from which data is to be drawn
        :return:
        """
        with open(file) as f:
            self.data = json.load(f)

    def flush(self) -> None:
        """
        Write the data to the JSON file
        """
        with open(self.location, mode='w') as output_file:
            json.dump(self.data, output_file)
            log.debug("Pipe %s wrote data %s to file %s",
                      self.__repr__(), self.data, self.location)

    @staticmethod
    def _make_quantities_serializable(data: dict) -> dict:
        for key in data.keys():
            value = data[key]

            if isinstance(value, Quantity):
                new_value = str(value)
                data[key] = new_value

        return data

    def __repr__(self):
        return "%s(location=%s)" % (self.__class__.__name__, self.location)
