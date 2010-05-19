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

        self.setCentralWidget(self.welcome_layout)
        self.setAttribute(QtCore.Qt.WA_Maemo5AutoOrientation, True)
        self.setWindowTitle("KhtEditor")

    def do_about(self):
        self.parent.about(self)

    def setupMain(self):
        self.welcome_layout = QtGui.QWidget()
        self._layout = QtGui.QVBoxLayout()
        
        self.label = QtGui.QLabel("KhtEditor")
        self._layout.addWidget(self.label)

        self._layout_button = QtGui.QHBoxLayout()        
        self.new_button = QtGui.QPushButton("New")
        self.open_button = QtGui.QPushButton("9pen")
        self._layout_button.addWidget(self.new_button)
        self._layout_button.addWidget(self.open_button)
        self._layout.addLayout(self._layout_button)
#        self.layout().addItem(self._layout)
        self.welcome_layout.setLayout(self._layout)

    def setupMenu(self):
        fileMenu = QtGui.QMenu(self.tr("&Menu"), self)
        self.menuBar().addMenu(fileMenu)

        fileMenu.addAction(self.tr("&New..."), self.parent.newFile,
                QtGui.QKeySequence(self.tr("Ctrl+N", "New")))
        fileMenu.addAction(self.tr("&Open..."), self.parent.openFile,
                QtGui.QKeySequence(self.tr("Ctrl+O", "Open")))
        fileMenu.addAction(self.tr("&About"), self.do_about)
