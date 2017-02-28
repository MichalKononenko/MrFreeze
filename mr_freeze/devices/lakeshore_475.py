"""
Contains methods for working with the Lakeshore 475 Gaussmeter
"""
from typing import Optional
from instruments.lakeshore import Lakeshore475 as _Lakeshore475


class Lakeshore475(object):
    """
    Adapter layer for IK's Lakeshore 475 implementation
    """
    _port = '/dev/ttyUSB0'
    _address = 12
    _managed_instance = None

    @property
    def portName(self) -> str:
        """

        :return: The port to which this magnetometer will be attached
        """
        return self._port

    @portName.setter
    def portName(self, new_port_name: str):
        """

        :param new_port_name: The new port
        :return:
        """
        self._port = new_port_name

    @property
    def address(self) -> int:
        """

        :return: The address
        """
        return self._address

    @address.setter
    def address(self, new_address: int):
        """

        :param new_address: The desired address
        :return:
        """
        self._address = new_address

    @property
    def magnetometer(self) -> Optional[_Lakeshore475]:
        """

        :return: The instance of the magnetometer that this adapter manages, or
            None if there is no instance.
        """
        if self._managed_instance is None:
            self._managed_instance = _Lakeshore475.open_gpibusb(
                port=self.portName, gpib_address=self.address)

        return self._managed_instance
