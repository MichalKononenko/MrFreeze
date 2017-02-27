"""
Contains methods for working with the Lakeshore 475 Gaussmeter
"""
from instruments.lakeshore import Lakeshore475 as _Lakeshore475


class LakeShore475GaussMeter(object):
    """
    Contains an adapter layer for IK's Lakeshore 475 implementation
    """
    _port = '/dev/ttyUSB0'
    _address = 12
    _managed_instance = None

    @property
    def portName(self):
        """

        :return: The port to which this magnetometer will be attached
        """
        return self._port

    @portName.setter
    def portName(self, newPortName):
        """

        :param newPortName: The new port
        :return:
        """
        self._port = newPortName

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, new_address):
        self._address = new_address

    @property
    def _communicator(self):
        return

    @property
    def magnetometer(self):
        """

        :return: The instance of the magnetometer that this adapter manages
        """
        if self._managed_instance is None:
            self._managed_instance = _Lakeshore475.open_gpibusb(
                port=self.portName, gpib_address=self.address)

        return self._managed_instance
