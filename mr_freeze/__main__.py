#!/usr/bin/env python
from mr_freeze.argument_parser import parser
from mr_freeze.main_loop import MainLoop

parsed_arguments = parser.parse_args()

loop = MainLoop(
    parsed_arguments.csv_file, parsed_arguments.ln2_gauge_address,
    parsed_arguments.gaussmeter_address, parsed_arguments.power_supply_address,
    parsed_arguments.sample_interval, parsed_arguments.task_timeout
)

loop.run()
