#!/usr/bin/python

import sys
import traceback
import urllib
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import khteditor

#APP_NAME = "Default App Name"
#APP_VERSION = "Default Version"

#Here is the installation of the hook. Each time a untrapped/unmanaged exception will
#happen my_excepthook will be called.
def install_excepthook(app_name,app_version):
#    global APP_NAME
#    global APP_VERSiON
#
#    APP_NAME = app_name
#    APP_VERSION = app_version
  
    def my_excepthook(exctype, value, tb):
        #traceback give us all the errors information message like the method, file line ... everything like
        #we have in the python interpreter 
        s = ''.join(traceback.format_exception(exctype, value, tb))
        formatted_text = "%s Version %s\nTrace : %s\nComments : " ('KhtEditor', str(khteditor.VERSION), s)
        #here is just my own gtk dialog you can replace it by what you want
        v = ReporterView()
        v.set_description(formatted_text)
        v.set_product_id('1,0,1')
        v.set_version(khteditor.VERSION)
        v.show()        
    sys.excepthook = my_excepthook

class ReporterView(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self,None)
        self.parent = parent

        self.setWindowTitle("KhtEditor Crash Reporter")

        self.w_root = QWidget()
        self._layout = QVBoxLayout()
        self.w_version = QLineEdit()
        self.w_description = QTextEdit()
        self.w_submit = QPushButton('send')
        self.connect(self.w_submit, SIGNAL('clicked()'),self.submit_report)
        self._layout.addWidget(self.w_version)
        self._layout.addWidget(self.w_description)
        self._layout.addWidget(self.w_submit)
        self.w_root.setLayout(self._layout)
        self.setCentralWidget(self.w_root)
        
    
    def submit_report(self):
        pass
        
    def set_description(self,formatted_text):
        pass

    def set_product_id(self,product_id):
        pass

    def set_version(self):
        self.w_version.setText(str(khteditor.VERSION))

class ReporterApp(QApplication):
    def __init__(self, argv):
        QApplication.__init__(self, argv)

        self.view = ReporterView()
        self.view.set_version()
        self.view.show()

if __name__=='__main__':
    app = ReporterApp(sys.argv)
    sys.exit(app.exec_())
        