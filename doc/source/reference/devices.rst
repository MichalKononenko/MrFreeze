Devices
=======

This section describes the devices that were implemented. The Lakeshore 475
gaussmeter has been implemented already in InstrumentKit.

Each device also contains an adapter for working with the device's IK
implementations.

The instruments implemented as of version 1.0 are
    - `Lakeshore 475`_ digital signal processing magnetometer
    - `Cryomagnetics 4G`_ superconducting magnet power supply
    - `Cryomagnetics LM-510`_ two-channel cryogen level meter


Device Adapters
---------------

Lakeshore 475
~~~~~~~~~~~~~

.. automodule:: mr_freeze.devices.lakeshore_475
    :members:
    :undoc-members:

Cryomagnetics 4G Power Supply
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: mr_freeze.devices.cryomagnetics_4g_adapter
    :members:
    :undoc-members:

Cryomagnetics LM-510 Level Meter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: mr_freeze.devices.cryomagnetics_lm510_adapter
    :members:
    :undoc-members:


Instrument Kit Devices
----------------------

Abstract Cryomagnetics Device
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: mr_freeze.devices.abstract_cryomagnetics_device
    :members:
    :undoc-members:

Cryomagnetics 4G Power Supply
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: mr_freeze.devices.cryomagnetics_4g
    :members:
    :undoc-members:

Cryomagnetics LM-510 Level Meter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: mr_freeze.devices.cryomagnetics_lm510
    :members:
    :undoc-members:

.. _Lakeshore 475: http://www.lakeshore.com/products/gaussmeters/model-475-dsp-gaussmeter/Pages/Overview.aspx
.. _Cryomagnetics 4G: http://www.cryomagnetics.com/products/model-4g-bipolar-power-supplies-superconducting-magnets/
.. _Cryomagnetics LM-510: http://www.cryomagnetics.com/products/model-lm-510-liquid-cryogen-monitor/