# -*- coding: utf-8
"""
Parses command line arguments given to the application
"""
import argparse
from mr_freeze.config_file_parser import ConfigFileParser

loader = ConfigFileParser()

parser = argparse.ArgumentParser(
    description="Log variables from the instrument rack"
)

parser.add_argument(
    '--gaussmeter-address', type=str,
    default=loader.gaussmeter_address,
    help="The address of the gaussmeter (example: /dev/ttyUSB0)"
)

parser.add_argument(
    '--power-supply-address', type=str,
    default=loader.power_supply_address,
    help="The address of the magnet power supply (example: /dev/ttyUSB0)"
)

parser.add_argument(
    '--ln2-gauge-address', type=str,
    default=loader.level_meter_address,
    help="The address of the liquid nitrogen level meter (example: "
         "/dev/ttyUSB0)"
)

parser.add_argument(
    '--csv-file', type=str,
    help="The name of the CSV file to which results will be written",
    default=loader.csv_output_directory
)

parser.add_argument(
    '--task-timeout', type=int,
    help="The maximum amount of time that can elapse before I/O is "
         "considered to have failed",
    default=loader.task_timeout
)

parser.add_argument(
    '--sample-interval', type=int,
    help="The amount of time in seconds that should elapse before making "
         "another measurement. By default, this value is 900 seconds (15 "
         "minutes)",
    default=loader.sample_interval
)

parser.add_argument(
    '--gui-only-mode', type=bool,
    help="Used only for testing, run if the GUI needs to be run without "
         "starting the measurement loop",
    default=False
)
