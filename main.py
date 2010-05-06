#!/usr/bin/env python

"""KhtEditor a source code editor by Khertan : Welcome Window"""

import sys
import welcome_window
from PyQt4 import QtCore, QtGui

class KhtEditor:
    def __init__(self):
      self.window_list = []
      self.app = QtGui.QApplication(sys.argv)

      self.run()

    def run(self):
      window = welcome_window.WelcomeWindow(None,self)
      window.show()

      sys.exit(self.app.exec_())
