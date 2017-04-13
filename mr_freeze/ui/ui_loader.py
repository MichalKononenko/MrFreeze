# -*- coding: utf-8 -*-
"""
Created on March 24, 2017

@author: Ishit Raval

Main file open when start.bat button is pressed   
"""

#################### Import necessary in built python module ###################
import sys
from PyQt4 import QtGui
import json
from time import sleep

from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from quantities import Quantity, cm

# IMPORTS For Gui setUp
from mr_freeze.ui.user_interface import Ui_MainwindowUI
from mr_freeze.resources.application_state import Store
from mr_freeze.resources.application_state import LiquidHeliumLevel
from mr_freeze.resources.application_state import LiquidNitrogenLevel
from mr_freeze.resources.application_state import MagneticField
from mr_freeze.resources.application_state import Current
from mr_freeze.resources.application_state import LoggingInterval

############################ IMPORTS For Gui Controller#############################
#from mr_freeze.main_loop import MainLoop
# from mr_freeze.argument_parser import parser
# from mr_freeze.main_loop import MainLoop
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
        self.ui.start_logging_button.clicked.connect(self.start)
        self.ui.stop_logging_button.clicked.connect(self.stop)
        self.ui.pushButton.clicked.connect(self.set_main_current)
        self.ui.pushButton_2.clicked.connect(self.sweep_current)
        self.ui.log_interval_go_button.clicked.connect(self.set_log_interval)
        self.interrupt = False

        self.store = store

        self._add_listeners(self.store)

    def start(self):
        """
        Start the application
        """
        print("Hello Mr freeze!!!!!")
        self.interrupt = True

        while self.interrupt:  # This constructs an infinite loop
            print("You enter")
            QtGui.qApp.processEvents()
            sleep(5)
            
        print("Stop logging")

    def stop(self):
        """
        Stop the application
        """
        print("Stop logging!!!")

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
    
    def get_json(self):
        with open('pipe.json') as data_file:    
            data = json.load(data_file)
        return data

    def closeEvent(self, event):

        quit_msg = "Are you sure you want to exit CSMC?"
        reply = QtGui.QMessageBox.question(self, 'Message', quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def _handle_lhe_level_change(self, new_value: Quantity) -> None:
        self.ui.liquid_helium_display.display(float(new_value))

    def _handle_ln2_level_change(self, new_value: Quantity) -> None:
        self.ui.liquid_nitrogen_display.display(float(new_value))

    def _handle_b_field_change(self, new_value: Quantity) -> None:
        self.ui.magnetic_field_display.display(float(new_value))

    def _handle_current_change(self, new_value: Quantity) -> None:
        self.ui.main_current_display.display(float(new_value))

    def _handle_logging_interval_change(self, new_value: Quantity) -> None:
        self.ui.log_interval_display.display(float(new_value))

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

    def _start_logging(self) -> None:
        """

        Start logging data
        """

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    with ThreadPoolExecutor(5 * cpu_count()) as executor:
        empty_store = Store(executor)
        window = Main(empty_store)
        window.show()
        sys.exit(app.exec_())
