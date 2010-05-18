#!/usr/bin/env python

"""KhtEditor a source code editor by Khertan : Welcome Window"""

import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
import editor_window

class WelcomeWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(QtGui.QMainWindow, self).__init__(parent)

        self.setupMenu()
        self.setupMain()

        self.setAttribute(QtCore.Qt.WA_Maemo5AutoOrientation, True)
        self.setWindowTitle("KhtEditor")

    def about(self):
        QtGui.QMessageBox.about(self, self.tr("About KhtEditor"),
                self.tr("<p><b>KhtEditor</b> is a source code editor "
                        "Mainly designed for Maemo and Meego.</p>"))

    def newFile(self):
        w = editor_window.Window()
        w.show()
        self.parent.window_list.append(w)

    def openFile(self, path=QtCore.QString()):
            editor_win=editor_window.Window(None,self.main)
            filename = editor_win.openFile(path)
            if not filename.isEmpty():
              editor_win.show()
            else:
              editor_win.destroy()

    def setupMain(self):
        self.layout = QtGui.QVBoxLayout()

    def setupMenu(self):
        fileMenu = QtGui.QMenu(self.tr("&Menu"), self)
        self.menuBar().addMenu(fileMenu)

        fileMenu.addAction(self.tr("&New..."), self.newFile,
                QtGui.QKeySequence(self.tr("Ctrl+N", "New")))
        fileMenu.addAction(self.tr("&Open..."), self.openFile,
                QtGui.QKeySequence(self.tr("Ctrl+O", "Open")))
        fileMenu.addAction(self.tr("&About"), self.about)
