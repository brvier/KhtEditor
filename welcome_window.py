#!/usr/bin/env python

"""KhtEditor a source code editor by Khertan : Welcome Window"""

import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
import editor_window

class WelcomeWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(QtGui.QMainWindow, self).__init__(None)
        self.parent = parent

        self.setupMenu()
        self.setupMain()

        self.setAttribute(QtCore.Qt.WA_Maemo5AutoOrientation, True)
        self.setWindowTitle("KhtEditor")

    def do_about(self):
        self.parent.about(self)

    def setupMain(self):
        self.layout = QtGui.QVBoxLayout()

    def setupMenu(self):
        fileMenu = QtGui.QMenu(self.tr("&Menu"), self)
        self.menuBar().addMenu(fileMenu)

        fileMenu.addAction(self.tr("&New..."), self.parent.newFile,
                QtGui.QKeySequence(self.tr("Ctrl+N", "New")))
        fileMenu.addAction(self.tr("&Open..."), self.parent.openFile,
                QtGui.QKeySequence(self.tr("Ctrl+O", "Open")))
        fileMenu.addAction(self.tr("&About"), self.do_about)
