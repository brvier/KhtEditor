#!/usr/bin/env python

"""KhtEditor a source code editor by Khertan : Welcome Window"""

import os
from PyQt4.QtGui import QMainWindow, \
    QSizePolicy, \
    QVBoxLayout, \
    QKeySequence, \
    QPushButton, \
    QHBoxLayout, \
    QWidget, \
    QMenu, \
    QLabel, \
    QPixmap, \
    QScrollArea

from PyQt4.QtCore import Qt
try:
    from PyQt4 import QtMaemo5
    isMAEMO = True
except:
    isMAEMO = False

from recent_files import RecentFiles


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
            del kwtmp["__max_args__"]
        print funcArgs
        
        return self.func(*funcArgs, **kwtmp)

class WelcomeWindow( QMainWindow):
    """
        The welcome window
    """
    
    def __init__(self, parent=None):
        QMainWindow.__init__(self,None)
        self.parent = parent
                 
        #This is for the case we aren't on Maemo
        try:
            self.setAttribute( Qt.WA_Maemo5AutoOrientation, True)
            self.setAttribute(Qt.WA_Maemo5StackedWindow, True)
            self.isMaemo = True
        except AttributeError:
            self.isMaemo = False
            self.resize(800,600)
        self.setupMain(self.isMaemo)
        self.setupMenu()        

        self.setCentralWidget(self.scrollArea)

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
                if self.isMaemo:
                    recentFileButton.setText(os.path.basename(unicode(recentfiles[index]).encode('utf-8')).decode('utf-8'))
                    recentFileButton.setValueText(os.path.abspath(unicode(recentfiles[index]).encode('utf-8')).decode('utf-8'))         
                else:
                    recentFileButton.setText(os.path.abspath(unicode(recentfiles[index]).encode('utf-8')).decode('utf-8'))

            except StandardError:
                recentFileButton.setDisabled(True)
        

    def setupMain(self, isMaemo=False):
        """
            GUI Initialization
        """
        
        self.scrollArea =  QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        awidget =  QWidget(self.scrollArea)
        if isMaemo:
            awidget.setMinimumSize(480,1000)
        awidget.setSizePolicy(  QSizePolicy.Expanding,  QSizePolicy.Expanding)
        self.scrollArea.setSizePolicy(  QSizePolicy.Expanding,  QSizePolicy.Expanding)
   
        #Kinetic scroller is available on Maemo and should be on meego
        try:
            scroller = self.scrollArea.property("kineticScroller") #.toPyObject()
            scroller.setEnabled(True)
        except:
            pass
            
        self._layout =  QVBoxLayout(awidget)
        
        self.icon =  QLabel()
        self.icon.setPixmap( QPixmap(os.path.join(os.path.dirname(__file__) ,'icons','khteditor.png')).scaledToHeight(64))
        self.icon.setAlignment( Qt.AlignCenter or Qt.AlignHCenter )
        self.icon.resize(70,70)
        
        self.label =  QLabel("KhtEditor Version "+self.parent.version)
        self.label.setAlignment( Qt.AlignCenter or Qt.AlignHCenter )

        self._layout.addWidget(self.icon)
        self._layout.addWidget(self.label)

        self._layout_button =  QHBoxLayout()        
        self.new_button =  QPushButton("New")
        self.new_button.clicked.connect(self.parent.newFile)
        self.open_button =  QPushButton("Open")
        self.open_button.clicked.connect(self.parent.openFile)
        self._layout_button.addWidget(self.new_button)
        self._layout_button.addWidget(self.open_button)
        self._layout.addLayout(self._layout_button)

        label =  QLabel("Recent Files")
        label.setAlignment( Qt.AlignCenter or Qt.AlignHCenter )

        self._layout.addWidget(label)

        awidget.setLayout(self._layout)
        self.scrollArea.setWidget(awidget)
        for index in range(10):
            if isMaemo:
                recentFileButton = QtMaemo5.QMaemo5ValueButton()
            else:
                recentFileButton =  QPushButton()
            recentFileButton.clicked.connect(Curry(self.openRecentFile,recentFileButton))
            self._layout.addWidget(recentFileButton)

    def openRecentFile(self,button, Useless=None):
        """
            Call back which open a recent file
        """
        
        if self.isMaemo:
            self.setAttribute( Qt.WA_Maemo5ShowProgressIndicator,True)
        self.parent.openRecentFile(button)
        if self.isMaemo:
            self.setAttribute( Qt.WA_Maemo5ShowProgressIndicator,False)

    def setupMenu(self):
        """
            Initialization of the maemo menu
        """
        
        fileMenu =  QMenu(self.tr("&Menu"), self)
        self.menuBar().addMenu(fileMenu)

        fileMenu.addAction(self.tr("&New..."), self.parent.newFile,
                 QKeySequence(self.tr("Ctrl+N", "New")))
        fileMenu.addAction(self.tr("&Open..."), self.parent.openFile,
                 QKeySequence(self.tr("Ctrl+O", "Open")))
        fileMenu.addAction(self.tr("&Preferences..."), self.showPrefs)
        fileMenu.addAction(self.tr("&About"), self.do_about)
        
    def showPrefs(self):
        """
            Call the parent class to show window
        """
        self.parent.showPrefs(self)
