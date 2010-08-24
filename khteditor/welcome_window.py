#!/usr/bin/env python

"""KhtEditor a source code editor by Khertan : Welcome Window"""

import os
from PyQt4 import QtCore, QtGui
try:
    from PyQt4 import QtMaemo5
    isMAEMO = True
except:
    isMAEMO = False
from PyQt4.QtCore import Qt
from recent_files import RecentFiles
import sys
import khteditor

class Curry:
    """keep a reference to all curried instances or they are immediately garbage collected"""
    instances = []
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.pending = args[:]
        self.kwargs = kwargs.copy()
        self.instances.append(self)
 
    def __call__(self, *args, **kwargs):
        """
            Call the right methods with right parameters
        """
        
        kwtmp = self.kwargs
        kwtmp.update(kwargs)
        funcArgs = self.pending + args
        #sometimes we want to limit the number of arguments that get passed,
        #calling the constructor with the option __max_args__ = n will limit
        #the function call args to the first n items
        maxArgs = kwtmp.get("__max_args__", -1)
        if maxArgs != -1:
            funcArgs = funcArgs[:maxArgs]
            delkwtmp["__max_args__"]
        return self.func(*funcArgs, **kwtmp)

class WelcomeWindow(QtGui.QMainWindow):
    """
        The welcome window
    """
    
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self,None)
        self.parent = parent

        self.setupMenu()
        self.setupMain()

        self.setCentralWidget(self.scrollArea)
        
        #This is for the case we aren't on Maemo
        if isMAEMO:
            self.setAttribute(QtCore.Qt.WA_Maemo5AutoOrientation, True)
            self.setAttribute(Qt.WA_Maemo5StackedWindow, True)
        self.setWindowTitle("KhtEditor")

    def do_about(self):
        """
            Display about dialog from parent
        """
        
        self.parent.about(self)

    def enterEvent(self,event):
        """
            Redefine the enter event to refresh recent file list
        """        
        self.refreshMain()
        
    def refreshMain(self):
        """
            Refresh the recent files list
        """
        
        recentfiles = RecentFiles().get()
        print self._layout.count()
        for index in range(0,self._layout.count()-4):
            recentFileButton = self._layout.itemAt(index+4).widget()
            try:
                recentFileButton.setText(os.path.basename(str(recentfiles[index])))
                recentFileButton.setValueText(os.path.abspath(str(recentfiles[index])))         
            except StandardError, e:
                recentFileButton.setDisabled(True)
        

    def setupMain(self):
        """
            GUI Initialization
        """
        
        self.scrollArea = QtGui.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        awidget = QtGui.QWidget(self.scrollArea)
        awidget.setMinimumSize(480,1000)
        awidget.setSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.scrollArea.setSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
   
        scroller = self.scrollArea.property("kineticScroller").toPyObject()
        scroller.setEnabled(True)

        self._layout = QtGui.QVBoxLayout(awidget)
        
        self.icon = QtGui.QLabel()
        self.icon.setPixmap(QtGui.QPixmap(os.path.join(khteditor.__path__[0],'icons','khteditor.png')).scaledToHeight(64))
        self.icon.setAlignment( Qt.AlignCenter or Qt.AlignHCenter )
        self.icon.resize(70,70)
        
        self.label = QtGui.QLabel("KhtEditor Version "+self.parent.version)
        self.label.setAlignment( Qt.AlignCenter or Qt.AlignHCenter )

        self._layout.addWidget(self.icon)
        self._layout.addWidget(self.label)

        self._layout_button = QtGui.QHBoxLayout()        
        self.new_button = QtGui.QPushButton("New")
        self.connect(self.new_button, QtCore.SIGNAL('clicked()'),self.parent.newFile)
        self.open_button = QtGui.QPushButton("Open")
        self.connect(self.open_button, QtCore.SIGNAL('clicked()'),self.parent.openFile)
        self._layout_button.addWidget(self.new_button)
        self._layout_button.addWidget(self.open_button)
        self._layout.addLayout(self._layout_button)

        label = QtGui.QLabel("Recent Files")
        label.setAlignment( Qt.AlignCenter or Qt.AlignHCenter )

        self._layout.addWidget(label)


        awidget.setLayout(self._layout)
        self.scrollArea.setWidget(awidget)
        recentfiles = RecentFiles().get()
        for index in range(10):
            recentFileButton = QtMaemo5.QMaemo5ValueButton()
            self.connect(recentFileButton, QtCore.SIGNAL('clicked()'), Curry(self.openRecentFile,recentFileButton))
            self._layout.addWidget(recentFileButton)

    def openRecentFile(self,button):
        """
            Call back which open a recent file
        """
        
        self.setAttribute(QtCore.Qt.WA_Maemo5ShowProgressIndicator,True)
        self.parent.openRecentFile(button)
        self.setAttribute(QtCore.Qt.WA_Maemo5ShowProgressIndicator,False)

    def setupMenu(self):$
        """
            Initialization of the maemo menu
        """
        
        fileMenu = QtGui.QMenu(self.tr("&Menu"), self)
        self.menuBar().addMenu(fileMenu)

        fileMenu.addAction(self.tr("&New..."), self.parent.newFile,
                QtGui.QKeySequence(self.tr("Ctrl+N", "New")))
        fileMenu.addAction(self.tr("&Open..."), self.parent.openFile,
                QtGui.QKeySequence(self.tr("Ctrl+O", "Open")))
        fileMenu.addAction(self.tr("&Preferences..."), self.showPrefs)
        fileMenu.addAction(self.tr("&About"), self.do_about)
        
    def showPrefs(self):
        """
            Call the parent class to show window
        """
        self.parent.showPrefs(self)
