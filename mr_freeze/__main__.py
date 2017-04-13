#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module called when the application is executed. Runs the argument parser and
starts the application loop
"""
from mr_freeze.bootloader import Application
import logging
import sys

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

logging.basicConfig(
    filename="logfile.log", level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Application()
exit_code = app.start()

sys.exit(exit_code)
