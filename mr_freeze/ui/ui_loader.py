# -*- coding: utf-8 -*-
'''
Created on March 24, 2017

@author: Ishit Raval

Main file open when start.bat button is pressed   
'''

#################### Import necessary in built python module ###################
import sys
from PyQt4 import QtGui
import json
from time import sleep


# IMPORTS For Gui setUp
from mr_freeze.ui.user_interface import Ui_MainwindowUI
from mr_freeze.argument_parser import parser

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
    def __init__(self, *args, **kwargs):
        QtGui.QMainWindow.__init__(self, *args, **kwargs)
        self.ui = Ui_MainwindowUI()
        self.ui.setupUi(self)
        # self.command_line_arguments = parser.parse_args()
        #self.bc = MainLoop()
        self.setWindowIcon(QtGui.QIcon("images/config.png"))
        self.ui.pushButton_4.clicked.connect(self.start)
        self.ui.pushButton_5.clicked.connect(self.stop)
        self.ui.pushButton.clicked.connect(self.set_main_current)
        self.ui.pushButton_2.clicked.connect(self.sweep_current)
        self.ui.pushButton_3.clicked.connect(self.set_log_interval)
        self.interrupt = False     

    def start(self):
        """
        Start the application
        """
        print("Hello Mr freeze!!!!!")
        self.interrupt = True

        while self.interrupt:  # This constructs an infinite loop
            print("You enter")
            
            data = self.get_json()
            self.ui.lcdNumber.display(self.get_num(data['Current']))
            self.ui.lcdNumber_5.display(self.get_num(data['Liquid Nitrogen Level']))
            self.ui.lcdNumber_3.display(self.get_num(data['Magnetic Field']))
            if not self.interrupt:
                break
            QtGui.qApp.processEvents()
            sleep(5)
            
        print("Stop logging")

    def stop(self):
        """
        Stop the application
        """
        print("Stop logging!!!")
        self.interrupt = False
        
        #self.bc.interrupt()
    
    def set_main_current(self):
        print("set_main_current")
    
    def sweep_current(self):
        print("sweep_current")
    
    def set_log_interval(self):
        print("set_log_interval")
        
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

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
