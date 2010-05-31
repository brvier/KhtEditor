#!/usr/bin/env python

"""KhtEditor a source code editor by Khertan : Welcome Window"""

import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
import editor_window
from recent_files import RecentFiles

class Curry:
  #keep a reference to all curried instances
  #or they are immediately garbage collected
  instances = []
  def __init__(self, func, *args, **kwargs):
    self.func = func
    self.pending = args[:]
    self.kwargs = kwargs.copy()
    self.instances.append(self)
 
  def __call__(self, *args, **kwargs):
    kw = self.kwargs
    kw.update(kwargs)
    funcArgs = self.pending + args
    #sometimes we want to limit the number of arguments that get passed,
    #calling the constructor with the option __max_args__ = n will limit
    #the function call args to the first n items
    maxArgs = kw.get("__max_args__", -1)
    if maxArgs != -1:
        funcArgs = funcArgs[:maxArgs]
        del kw["__max_args__"]
    return self.func(*funcArgs, **kw)

class WelcomeWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self,None)
        self.parent = parent

        self.setupMenu()
        self.setupMain()

        self.setCentralWidget(self.welcome_layout)
 	#TODO : Test if on maemo or not
        self.setAttribute(QtCore.Qt.WA_Maemo5AutoOrientation, True)
        self.setAttribute(Qt.WA_Maemo5StackedWindow, True)
        self.setWindowTitle("KhtEditor")

    def do_about(self):
        self.parent.about(self)

    def setupMain(self):
        self.welcome_layout = QtGui.QWidget()
        self._layout = QtGui.QVBoxLayout()
        
        self.label = QtGui.QLabel("KhtEditor Version "+self.parent.version)
        self.label.setAlignment( Qt.AlignCenter or Qt.AlignHCenter )

        self._layout.addWidget(self.label)

        self._layout_button = QtGui.QHBoxLayout()        
        self.new_button = QtGui.QPushButton("New")
        self.connect(self.new_button, QtCore.SIGNAL('clicked()'),self.parent.newFile)
        self.open_button = QtGui.QPushButton("Open")
        self.connect(self.open_button, QtCore.SIGNAL('clicked()'),self.parent.openFile)
        self._layout_button.addWidget(self.new_button)
        self._layout_button.addWidget(self.open_button)
        self._layout.addLayout(self._layout_button)
#        self.layout().addItem(self._layout)
        self.welcome_layout.setLayout(self._layout)
        
        for recentFile in RecentFiles().get():
            recentFileButton = QtGui.QPushButton(recentFile)
            self.connect(recentFileButton, QtCore.SIGNAL('clicked()'), Curry(self.parent.openRecentFile,recentFile))
            self._layout.addWidget(recentFileButton)

    def setupMenu(self):
        fileMenu = QtGui.QMenu(self.tr("&Menu"), self)
        self.menuBar().addMenu(fileMenu)

        fileMenu.addAction(self.tr("&New..."), self.parent.newFile,
                QtGui.QKeySequence(self.tr("Ctrl+N", "New")))
        fileMenu.addAction(self.tr("&Open..."), self.parent.openFile,
                QtGui.QKeySequence(self.tr("Ctrl+O", "Open")))
        fileMenu.addAction(self.tr("&About"), self.do_about)