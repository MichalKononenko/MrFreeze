#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module called when the application is executed. Runs the argument parser and
starts the application loop
"""
from mr_freeze.argument_parser import parser
from mr_freeze.main_loop import MainLoop
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

logging.basicConfig(
    filename="logfile.log", level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

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
    parsed_arguments.csv_file, parsed_arguments.json_file,
    parsed_arguments.ln2_gauge_address,
    parsed_arguments.gaussmeter_address,
    parsed_arguments.power_supply_address,
    parsed_arguments.sample_interval,
    parsed_arguments.task_timeout
)

loop.run()
