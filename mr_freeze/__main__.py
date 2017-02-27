"""
Contains the execution script
"""
from mr_freeze.control_scripts.field_logging import FieldLogger
from mr_freeze.devices.lakeshore_475 import LakeShore475GaussMeter
from threading import Thread

meter = LakeShore475GaussMeter()
meter.portName = '/dev/ttyUSB0'

fieldLogger = FieldLogger(meter.magnetometer)

pollingThread = Thread(target=fieldLogger.__call__)

pollingThread.start()
