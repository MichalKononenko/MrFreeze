#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on March 24, 2017

@author: Ishit Raval

Main file open when start.bat button is pressed   
"""

#################### Import necessary in built python module ###################
import sys
from PyQt4 import QtGui
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from quantities import Quantity, cm
from random import uniform
import os
from datetime import datetime
from threading import Thread
import schedule

# IMPORTS For Gui setUp
from mr_freeze.ui.user_interface import Ui_MainwindowUI
from mr_freeze.resources.csv_file import CSVLogger
from mr_freeze.resources.application_state import Store
from mr_freeze.resources.application_state import LiquidHeliumLevel
from mr_freeze.resources.application_state import LiquidNitrogenLevel
from mr_freeze.resources.application_state import MagneticField
from mr_freeze.resources.application_state import Current
from mr_freeze.resources.application_state import LoggingInterval
from mr_freeze.resources.application_state import CSVDirectory

############################ IMPORTS For Gui Controller#############################
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

logging.basicConfig(
    filename="logfile.log", level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class Main(QtGui.QMainWindow):
    """
    Contains the connected UI application
    """
    def __init__(self, store: Store, *args, **kwargs):
        QtGui.QMainWindow.__init__(self, *args, **kwargs)
        self.ui = Ui_MainwindowUI()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("images/config.png"))
        self.ui.start_logging_button.clicked.connect(self.start_logging)
        self.ui.stop_logging_button.clicked.connect(self.stop_logging)
        self.ui.pushButton_2.clicked.connect(self.sweep_current)
        self.ui.log_interval_go_button.clicked.connect(self.set_log_interval)
        self.interrupt = False

        self.store = store

        self._add_listeners(self.store)
        self._csv_log = None
        self.ui.stop_logging_button.setDisabled(True)

    def start_logging(self):
        """
        Start the application
        """
        path_to_csv_file = os.path.join(
            self.store[CSVDirectory].value,
            "result-%s" % datetime.now().isoformat()
        )
        csv_log = CSVLogger(self.store, path_to_csv_file, self.store.executor)
        csv_log.start_logging()

        self._csv_log = csv_log
        self.ui.start_logging_button.setDisabled(True)
        self.ui.stop_logging_button.setEnabled(True)

    def stop_logging(self):
        """
        Stop the application
        """
        if self._csv_log is not None:
            self._csv_log.stop_logging()
            self._csv_log = None
            self.ui.start_logging_button.setEnabled(True)
            self.ui.stop_logging_button.setDisabled(True)

    def set_main_current(self):
        print("set_main_current")
    
    def sweep_current(self):
        print("sweep_current")
    
    def set_log_interval(self):
        """
        Set the log interval to a new value
        """
        log_text = self.ui.log_interval_textbox.text()

        try:
            log_interval = float(log_text)
        except ValueError:
            QtGui.QMessageBox.warning(
                self, 'Error',
                '%s is not a number' % log_text,
                QtGui.QMessageBox.Ok
            )
            return

        self.store[LoggingInterval].value = log_interval

    def get_num(self,num):
        a = num.split(" ")
        return a[0]

    def closeEvent(self, event):

        quit_msg = "Are you sure you want to exit CSMC?"
        reply = QtGui.QMessageBox.question(self, 'Message', quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def _handle_lhe_level_change(self, new_value: Quantity) -> None:
        log.debug(
            "UI received Handle LHe Change event. New value is %s",
            new_value
        )
        self.ui.lhe_level_display.setText("%2.4f" % float(new_value))

    def _handle_ln2_level_change(self, new_value: Quantity) -> None:
        log.debug(
            "UI received LN2 change event. New value is %s",
            new_value
        )
        self.ui.ln2_level_display.setText("%2.4f" % float(new_value))

    def _handle_b_field_change(self, new_value: Quantity) -> None:
        log.debug(
            "UI received B field change event. New value is %s",
            new_value
        )
        self.ui.magnetic_field_display.setText("%2.4f" % float(new_value))

    def _handle_current_change(self, new_value: Quantity) -> None:
        log.debug(
            "UI received Current change event. New value is %s",
            new_value
        )
        self.ui.main_current_display.setText("%2.4f" % float(new_value))

    def _handle_logging_interval_change(self, new_value: Quantity) -> None:
        self.ui.log_interval_display.setText("%2.4f" % float(new_value))

    def _add_listeners(self, store: Store) -> None:
        """
        Hook up the handlers to the store in order to handle changes in the
        store

        :param store: The store to use to update the listeners
        :return:
        """
        store[LiquidHeliumLevel].listeners.add(self._handle_lhe_level_change)
        store[LiquidNitrogenLevel].listeners.add(self._handle_ln2_level_change)
        store[MagneticField].listeners.add(self._handle_b_field_change)
        store[Current].listeners.add(self._handle_current_change)
        store[LoggingInterval].listeners.add(
            self._handle_logging_interval_change
        )


def change_event(store: Store):
    """
    Change a few values to show that the UI store is working as expected

    :param store:
    :return:
    """
    while True:
        sleep(0.25)
        store[LiquidHeliumLevel].value = uniform(0, 100.0) * cm
        store[LiquidNitrogenLevel].value = uniform(0, 100.0) * cm
        store[MagneticField].value = uniform(0, 10.0)
        store[Current].value = uniform(0, 100.0)


class SchedulerThread(Thread):
    """
    runs the scheduler
    """
    def run(self) -> None:
        """
        Run the scheduler

        :return:
        """
        while True:
            sleep(1)
            schedule.run_pending()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    scheduler_thread = SchedulerThread(daemon=True)
    scheduler_thread.start()

    with ThreadPoolExecutor(5 * cpu_count()) as executor:
        empty_store = Store(executor)

        empty_store[CSVDirectory].value = os.path.abspath(os.path.curdir)

        window = Main(empty_store)
        window.show()
        task = executor.submit(change_event, empty_store)
        sys.exit(app.exec_())
