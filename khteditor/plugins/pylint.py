#!/usr/bin/env python

"""PyLint Plugin : A KhtEditor plugin to lint current source code and
   And display the result"""

#PYLINT:W:Unused import QThread
#PYLINT:W:Unused import Qt
#PYLINT:C:Comma not followed by a space
#PYLINT:C:Missing docstring
from PyQt4.QtCore import Qt, \
                         QProcess, \
                         QRegExp, \
                         SIGNAL, \
                         QString, \
                         QObject, \
                         QAbstractListModel, \
                         QModelIndex, \
                         QVariant \

from PyQt4.QtGui import QAction, \
                        QIcon, \
                        QMainWindow, \
                        QListView \
                        
import PyQt4.QtMaemo5 #Not really unused as it s import to Qt
import PyQt4.Qt
try:
    from plugins_api import Plugin
except:
    from khteditor.plugins.plugins_api import Plugin
        
import os.path
import sys

class PyLint_ResultModel(QAbstractListModel):
    """ ListModel : The lint result model"""

    def __init__(self, mlist=[]):
        QAbstractListModel.__init__(self)

        # Cache the passed data list as a class member.
        self._items = mlist

    def rowCount(self, parent = QModelIndex()):
        return len(self._items)
        
    def setData(self,mlist):
        try:
            if len(mlist[0])==3:
                self._items = mlist
                QObject.emit(self, \
                    SIGNAL("dataChanged(const QModelIndex&, const QModelIndex &)"), \
                    self.createIndex(0,0),\
                    self.createIndex(0,len(self._items)))
        except StandardError,e:
            print e 
            
    def appendData(self,mlist):
        try:
            if len(mlist[0])==3:
                self._items = self._items + mlist
                QObject.emit(self, \
                    SIGNAL("dataChanged(const QModelIndex&, const QModelIndex &)"), \
                    self.createIndex(0,0), \
                    self.createIndex(0,len(self._items)))
        except StandardError,e:
            print e 
            
    def data(self, index, role = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            text = self._items[index.row()][0] \
                + ':L' + self._items[index.row()][1] \
                + ' : ' + self._items[index.row()][2]
            return QVariant(text)
        else:
            return QVariant()
           
class PyLint_Result(QMainWindow):
    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)
        self.parent = parent
        self.setAttribute(Qt.WA_Maemo5AutoOrientation, True)
        
        self.listView = QListView()
        self.listModel = PyLint_ResultModel()
        self.listView.setViewMode(QListView.ListMode)
        self.listView.setWordWrap(True)
        self.listView.setResizeMode(QListView.Adjust)
        self.listView.setModel(self.listModel)
        self.setCentralWidget(self.listView)
        
    def setResult(self,results):
        self.listModel.setData(results)
        
    def appendResult(self,results):
        self.listModel.appendData(results)
        
class PyLint(Plugin, QObject):
    """ PyLint Plugin """
    capabilities = ['toolbarHook']
    __version__ = '0.2'
    thread = None
    
    def do_toolbarHook(self,parent):
        """ Hook to install the pylint toolbar button"""
        self.parent = parent
        
        #Keep a references to prevent gc 
        #deleting our callback methode
        try:
            self.parent.plugins_ref.append(self)
        except:
            self.parent.plugins_ref = [self,]
            
        icon = QIcon(os.path.join(sys.path[0], \
            'icons/tb_pylint.png'))
        print 'test'
        self.parent.tb_pylint = QAction('PyLint', self.parent)          
        self.connect(self.parent.tb_pylint, \
            SIGNAL('triggered()'), \
            self.do_pylint)
        self.parent.toolbar.addAction(self.parent.tb_pylint)
        
    def do_pylint(self):
        """ Launch the lint process and create the result window """
        print 'do_pylint'

        self.pylintProc = QProcess()

        self.pylintProc.setProcessChannelMode(QProcess.MergedChannels)
        self.pylintProc.setWorkingDirectory( \
            os.path.dirname(str(self.parent.editor.filename)))
        self.pylintProc.setReadChannel(QProcess.StandardOutput)

        self.connect(self.pylintProc, \
            SIGNAL('finished(int)'), \
            self.finished)
        self.connect(self.pylintProc, \
            SIGNAL('readyReadStandardOutput()'), \
            self.handleStdout)
        self.connect(self.pylintProc, \
            SIGNAL('readyReadStandardError()'), \
            self.handleStderr)
        if (self.pylintProc.start("pylint", \
                [self.parent.editor.filename,])):
            print 'Cannot start process'

        self.win = PyLint_Result()
        self.win.setWindowTitle("PyLint Results :" \
            + self.parent.editor.filename)
        self.win.show()
        self.win.setAttribute(Qt.WA_Maemo5ShowProgressIndicator,True)
        self.win.connect(self.win.listView, \
            SIGNAL('doubleClicked(const QModelIndex&)'), \
            self.gotoLine)

        self.pylintProc.waitForStarted()
        
    def finished(self,int):
        """ Call back called when lint end """
        self.win.setAttribute(Qt.WA_Maemo5ShowProgressIndicator,False)
        
    def handleStdout(self):
        """
        Private slot to handle the readyReadStdout
        signal of the pylint process.
        """
        resultList = []
        while self.pylintProc and self.pylintProc.canReadLine():
            result = self.pylintProc.readLine()
            if result != None:
                print 'DEBUG:',result
                result = QString(result)
                regex = QRegExp('(\w):(.*):.*: (.*)')
                regex_score = \
                    QRegExp('.*at (\d.\d*)/10.*')
                pos = 0
                inserted_line = 0
                while True:
                    pos = regex.indexIn(result,pos)
                    if pos<0:
                        if regex_score.indexIn(result,0)>=0:
                            self.win.setWindowTitle( \
                                "PyLint Results :" \
                                + str(regex.cap(1))
                                + self.parent.editor.filename)
                        break
                    line = int(regex.cap(2))
                    resultList.append((regex.cap(1),regex.cap(2),regex.cap(3)))
                    pos = pos + regex.matchedLength()
                    
        if len(resultList)>0:
            self.win.appendResult(resultList)
        
    def gotoLine(self,index):
        """ Callback called when a lint result is double clicked """
        line = int(self.win.listModel._items[index.row()][1])
        self.parent.do_gotoLine(line)
        
    def handleStderr(self):
        """
        Private slot to handle the readyReadStderr
        signal of the pylint process. Currently not
        managed
        """
        print 'error stderr'
