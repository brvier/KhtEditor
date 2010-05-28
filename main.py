#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""KhtEditor a source code editor by Khertan : Welcome Window"""

VERSION = '0.0.1'

import sys
import welcome_window
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
import editor_window

class KhtEditor:
    def __init__(self):
      self.window_list = []
      self.version = VERSION

      self.app = QtGui.QApplication(sys.argv)
      self.run()

    def run(self):
      window = welcome_window.WelcomeWindow(self)
      window.show()

      sys.exit(self.app.exec_())
      
    def about(self,widget):
        #QtGui.QMessageBox.about(widget, ("About KhtEditor"),
        #        ("<p><b>KhtEditor</b> is a source code editor "
        #                "Mainly designed for Maemo and Meego.</p>"))
        aboutWin = QtGui.QMainWindow(widget)
        aboutWin.setAttribute(Qt.WA_Maemo5StackedWindow, True)
        aboutWin.setAttribute(Qt.WA_Maemo5AutoOrientation, True)
        aboutLabel = QtGui.QLabel('<center><b>KhtEditor</b> %s<br><br>A source code editor designed for ease of use on small screen<br><br>By Beno&icirc;t HERVIER (Khertan) </center>' % self.version)
        aboutWin.setWindowTitle('About KhtEditor')
        aboutWin.setCentralWidget(aboutLabel)
        aboutWin.show()
        
    def newFile(self):
        editor_win = editor_window.Window(self)
        editor_win.show()
        self.window_list.append(editor_win)

    def openFile(self, path=QtCore.QString()):
            editor_win=editor_window.Window(self)
            filename = editor_win.openFile(path)
            if not filename.isEmpty():
              editor_win.show()
              self.window_list.append(editor_win)
            else:
              editor_win.destroy()


if __name__ == '__main__':
    KhtEditor()
