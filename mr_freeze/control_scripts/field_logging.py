"""
Contains a simple logger that dumps output of the gaussmeter to standard out
"""
from time import sleep

class FieldLogger(object):
    """
    Implements an algorithm for running the logger
    """
    polling_interval_in_seconds = 3

    def __init__(self, gauge):
        """
        Instantiate the object

        :param gauge: The gauge to use for the logging
        """
        self.gauge = gauge
        self.can_run = True

    def __call__(self):
        """

        Run the algorithm
        """
        while self.can_run:
            fieldStrength = self._field_strength
            self._write_field_strength(fieldStrength)
            self._wait_for_polling_interval()

    def interrupt(self):
        self.can_run = False

    @property
    def _field_strength(self):
        return self.gauge.field

    @staticmethod
    def _write_field_strength(field_strength):
        print("B = %s" % field_strength)

    def _wait_for_polling_interval(self):
        sleep(self.polling_interval_in_seconds)
