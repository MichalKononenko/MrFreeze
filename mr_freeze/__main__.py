#!/usr/bin/env python
"""
Contains the execution script
"""
from concurrent.futures import ThreadPoolExecutor
from mr_freeze.devices.lakeshore_475 import Lakeshore475
from mr_freeze.tasks.report_magnetic_field import ReportMagneticField

meter = Lakeshore475()
meter.port_name = '/dev/ttyUSB0'

executor = ThreadPoolExecutor(1)

b_task = ReportMagneticField(meter)

print("B = %s" % b_task(executor).result())
