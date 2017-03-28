# coding=utf-8
"""
Describes a pipe that can be used to write the last sample live
"""
import json


class Pipe(object):
    """
    Describes a FIFO pipe of samples that are to be written to the device
    """
    def __init__(self, location: str) -> None:
        self.location = location
        self.data = {}

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
