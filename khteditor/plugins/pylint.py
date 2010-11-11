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
                         QObject, \
                         QAbstractListModel, \
                         QModelIndex

from PyQt4.QtGui import QAction, \
                        QMainWindow, \
                        QListView 
                        
try:                        
    import PyQt4.QtMaemo5 #Not really unused as it s import to Qt
    isMAEMO = True
except:
    isMAEMO = False
    
try:
    from plugins_api import Plugin
except:
    from khteditor.plugins.plugins_api import Plugin
        
import os.path
import sys

class ResultModel(QAbstractListModel):
    """ list_model : The lint result model"""

    def __init__(self):        
        QAbstractListModel.__init__(self)

        # Cache the passed data list as a class member.
        self.items = []

    def rowCount(self, parent = QModelIndex()):
        """ Row count from Qlist_model """
        return len(self.items)
        
    def set_data(self, mlist):
        """ Set data from a tuple in the model """
        try:
            if len(mlist[0])==3:
                self.items = mlist
                QObject.emit(self, \
                    SIGNAL("dataChanged(const QModelIndex&, const QModelIndex &)"), self.createIndex(0,0), self.createIndex(0,len(self.items))) # pylint: disable=C0301
        except StandardError:
            pass
            
    def append_data(self, mlist):
        """ Append data from a tuple in the model """
        try:
            if len(mlist[0])==3:
                self.items = self.items + mlist
                QObject.emit(self, \
                    SIGNAL("dataChanged(const QModelIndex&, const QModelIndex &)"), self.createIndex(0,0), self.createIndex(0,len(self.items))) # pylint: disable=C0301
        except StandardError:
            pass
            
    def data(self, index, role = Qt.DisplayRole):
        """ Get data in the model """
        if role == Qt.DisplayRole:
            text = self.items[index.row()][0] \
                + ':L' + self.items[index.row()][1] \
                + ' : ' + self.items[index.row()][2]
            return text
        else:
            return None
           
class ResultWin(QMainWindow):
    """ Window use to display pylint results """
    
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.parent = parent
        try:
            self.setAttribute(Qt.WA_Maemo5AutoOrientation, True)
        except:
            pass
        self.list_view = QListView()
        self.list_model = ResultModel()
        self.list_view.setViewMode(QListView.ListMode)
        self.list_view.setWordWrap(True)
        self.list_view.setResizeMode(QListView.Adjust)
        self.list_view.setModel(self.list_model)
        self.setCentralWidget(self.list_view)
        
    def set_results(self, results):
        """ Set the tuple in the model """
        self.list_model.set_data(results)
        
    def append_results(self, results):
        """ Append the tuple in the model """
        self.list_model.append_data(results)
        
class PyLint(Plugin, QObject):
    """ PyLint Plugin """
    capabilities = ['toolbarHook']
    __version__ = '0.3'
    thread = None
    
    def do_toolbarHook(self, parent):
        """ Hook to install the pylint toolbar button"""
        self.parent = parent
        
        #Keep a references to prevent gc 
        #deleting our callback methode
        try:
            self.parent.plugins_ref.append(self)
        except StandardError:            
            self.parent.plugins_ref = [self, ]
            
#        icon = QIcon(os.path.join(sys.path[0], \
#            'icons/tb_pylint.png'))
        print 'test'
        self.parent.tb_pylint = QAction('PyLint', self.parent)          
        self.connect(self.parent.tb_pylint, \
            SIGNAL('triggered()'), \
            self.do_pylint)
        self.parent.toolbar.addAction(self.parent.tb_pylint)
        
    def do_pylint(self):
        """ Launch the lint process and create the result window """
        print 'do_pylint'

        self.pylint_pross = QProcess()
        self.pylint_pross.setProcessChannelMode(QProcess.MergedChannels)
        self.pylint_pross.setWorkingDirectory( \
            os.path.dirname(str(self.parent.editor.filename)))
        self.pylint_pross.setReadChannel(QProcess.StandardOutput)

        self.connect(self.pylint_pross, \
            SIGNAL('finished(int)'), \
            self.finished)
        self.connect(self.pylint_pross, \
            SIGNAL('readyReadStandardOutput()'), \
            self.handle_stdout)
        self.connect(self.pylint_pross, \
            SIGNAL('readyReadStandardError()'), \
            self.handle_stderr)
        if (self.pylint_pross.start("pylint", \
                [self.parent.editor.filename,])):
            print 'Cannot start process'

        self.win = ResultWin()
        self.win.setWindowTitle("PyLint Results :" \
            + os.path.basename(str(self.parent.editor.filename)))
        self.win.show()
        if isMAEMO:
            self.win.setAttribute(Qt.WA_Maemo5ShowProgressIndicator, True)
            
        self.win.connect(self.win.list_view, \
            SIGNAL('doubleClicked(const QModelIndex&)'), \
            self.goto_line)

        self.pylint_pross.waitForStarted()
        
    def finished(self, _):
        """ Call back called when lint end """
        if isMAEMO:
            self.win.setAttribute(Qt.WA_Maemo5ShowProgressIndicator, False)
            
    def handle_stdout(self):
        """
        Private slot to handle the readyReadStdout
        signal of the pylint process.
        """
        result_list = []
        #regex = QRegExp('(\w)\S*:\S*(\d*):.*: (.*)')
        regex = QRegExp('(\w)\s*:\s*(\d*):(.*)')
        regex_score = \
            QRegExp('.*at.(\d.\d*)/10.*')
        while self.pylint_pross and self.pylint_pross.canReadLine():
            result = unicode(self.pylint_pross.readLine())
            if result != None:
                pos = 0
                while True:
                    pos = regex.indexIn(result, pos)
                    if pos < 0:
                        if regex_score.indexIn(result, 0) >= 0:
                            self.win.setWindowTitle( \
                                "PyLint Results :" \
                                + str(regex_score.cap(1)) \
                                + ':'                                
                                + os.path.basename(str(self.parent.editor.filename)))
                        break
                    result_list.append((regex.cap(1), regex.cap(2), regex.cap(3)))
                    #print 'Append : ',(regex.cap(1), regex.cap(2), regex.cap(3))
                    pos = pos + regex.matchedLength()
                    
        if len(result_list)>0:
            self.win.append_results(result_list)
        
    def goto_line(self, index):
        """ Callback called when a lint result is double clicked """
        line = int(self.win.list_model.items[index.row()][1])
        self.parent.do_gotoLine(line)
        
    def handle_stderr(self):
        """
        Private slot to handle the readyReadStderr
        signal of the pylint process. Currently not
        managed
        """
        print 'error stderr'
