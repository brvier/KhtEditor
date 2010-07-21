#!/usr/bin/python

import sys
import traceback
import urllib
from PyQt4.QtGui import *
 
APP_NAME = "Default App Name"
APP_VERSION = "Default Version"

#Here is the installation of the hook. Each time a untrapped/unmanaged exception will
#happen my_excepthook will be called.
def install_excepthook(app_name,app_version):
    global APP_NAME
    global APP_VERSiON

    APP_NAME = app_name
    APP_VERSION = app_version
  
    def my_excepthook(exctype, value, tb):
        #traceback give us all the errors information message like the method, file line ... everything like
        #we have in the python interpreter 
        s = ''.join(traceback.format_exception(exctype, value, tb))
        formatted_text = "%s Version %s\nTrace : %s\nComments : " (str(APP_NAME), str(APP_VERSION), s)
        #here is just my own gtk dialog you can replace it by what you want
        ErrorReportDialog(formatted_text)

    sys.excepthook = my_excepthook

class ReporterView(QMainWindow):
    def __init__(self):
        super(self)
        
    def      
        
if __name__ == "__main__":
    v = ReporterView()
