"""
Parses command line arguments given to the application
"""
import argparse
import os
from datetime import datetime

parser = argparse.ArgumentParser(
    description="Log variables from the instrument rack"
)

parser.add_argument(
    '--gaussmeter-address', type=str,
    default='/dev/ttyUSB0',
    help="The address of the gaussmeter (example: /dev/ttyUSB0)"
)

parser.add_argument(
    '--power-supply-address', type=str,
    default='/dev/ttyUSB1',
    help="The address of the magnet power supply (example: /dev/ttyUSB0)"
)

parser.add_argument(
    '--ln2-gauge-address', type=str,
    default='/dev/ttyUSB2',
    help="The address of the liquid nitrogen level meter (example: "
         "/dev/ttyUSB0)"
)

parser.add_argument(
    '--csv-file', type=str,
    help="The name of the CSV file to which results will be written",
    default=os.path.join(os.curdir, "result-%s.csv" % datetime.now())
)

parser.add_argument(
    '--json-file', type=str,
    help="The name of the JSON file to which the last measured result will "
         "be written. By default, this file is ./pipe.json",
    default=os.path.join(os.curdir, "pipe.json")
)

parser.add_argument(
    '--task-timeout', type=int,
    help="The maximum amount of time that can elapse before I/O is "
         "considered to have failed",
    default=10
)

parser.add_argument(
    '--sample-interval', type=int,
    help="The amount of time in seconds that should elapse before making "
         "another measurement. By default, this value is 900 seconds (15 "
         "minutes)",
    default=900
)
