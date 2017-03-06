#!/usr/bin/env python
"""
Module called when the application is executed. Runs the argument parser and
starts the application loop
"""
from mr_freeze.argument_parser import parser
from mr_freeze.main_loop import MainLoop
import logging
import sys

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
ch.setFormatter(formatter)
log.addHandler(ch)


parsed_arguments = parser.parse_args()

if any(
        (variable is None for variable in {
            parsed_arguments.csv_file,
            parsed_arguments.ln2_gauge_address,
            parsed_arguments.gaussmeter_address,
            parsed_arguments.power_supply_address,
            parsed_arguments.sample_interval,
            parsed_arguments.task_timeout
        })
):
    parser.print_usage()

loop = MainLoop(
    parsed_arguments.csv_file, parsed_arguments.ln2_gauge_address,
    parsed_arguments.gaussmeter_address, parsed_arguments.power_supply_address,
    parsed_arguments.sample_interval, parsed_arguments.task_timeout
)

loop.run()
