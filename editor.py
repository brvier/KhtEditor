#!/usr/bin/env python

"""KhtEditor a source code editor by Khertan : Code Editor"""

import sys
import re
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from plugins import init_plugin_system, get_plugins_by_capability

class Kht_Editor(QtGui.QTextEdit):
    def __init__(self, parent=None, fileName=QtCore.QString('')):
        QtGui.QTextEdit.__init__(self,parent)
        init_plugin_system({'plugin_path': './plugins', 'plugins': ['autoindent']})
        self.fileName = fileName
        if self.fileName.isEmpty():
            self.fileName = QtCore.QString("Unnamed.txt")
        self.document().setModified(False)

        parent.setWindowTitle(self.fileName)
        print self.dynamicPropertyNames()
        self.kineticScroller = True
        self.setProperty("FingerScrollable", True)
        self.setProperty("kineticScroller", True) 
#        self.setTextInteractionFlags(Qt.TextBrowserInteraction) 

        self.setLineWrapMode(QtGui.QTextEdit.NoWrap)

    def keyPressEvent(self, e):
        for plugin in get_plugins_by_capability('beforeKeyPressEvent'):
            plg = plugin()
            plg.do_beforeKeyPressEvent(self,e)
        QtGui.QTextEdit.keyPressEvent(self, e)
        for plugin in get_plugins_by_capability('afterKeyPressEvent'):
            plg = plugin()
            plg.do_afterKeyPressEvent(self,e)

    def closeEvent(self):
        print 'closeEvent called'
        if self.document().isModified() and \
           QtGui.QMessageBox.question(self,
                   "Text Editor - Unsaved Changes",
                   "Save unsaved changes in %s?" % self.fileName,
                   QtGui.QMessageBox.Yes|QtGui.QMessageBox.No) == \
                QtGui.QMessageBox.Yes:
            try:
                self.save()
            except (IOError, OSError), e:
                QtGui.QMessageBox.warning(self, "Text Editor -- Save Error",
                        "Failed to save %s: %s" % (self.fileName, e))

    def save(self):
        if self.fileName.startsWith("Unnamed"):
            fileName = QtGui.QFileDialog.getSaveFileName(self,
                            "Text Editor -- Save File As",
                            self.fileName, "Text files (*.txt *.*)")
            if fileName.isEmpty():
                return
            self.fileName = fileName
        self.setWindowTitle(QtCore.QFileInfo(self.fileName).fileName())
        exception = None
        fh = None
        try:
            fh = QtCore.QFile(self.fileName)
            if not fh.open(QtCore.QIODevice.WriteOnly):
                raise IOError, unicode(fh.errorString())
            stream = QtCore.QTextStream(fh)
            stream.setCodec("UTF-8")
            stream << self.toPlainText()
            self.document().setModified(False)
        except (IOError, OSError), e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception


    def load(self):
        exception = None
        fh = None
        try:
            fh = QtCore.QFile(self.fileName)
            if not fh.open(QtCore.QIODevice.ReadOnly):
                raise IOError, unicode(fh.errorString())
            stream = QtCore.QTextStream(fh)
            stream.setCodec("UTF-8")
            self.setPlainText(stream.readAll())
            self.document().setModified(False)
            self.setWindowTitle(QtCore.QFileInfo(self.fileName).fileName())
        except (IOError, OSError), e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception

    def isModified(self):
        return self.document().isModified()

