#!/usr/bin/env python

"""KhtEditor a source code editor by Khertan : Code Editor"""

import re
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from plugins import init_plugin_system, get_plugins_by_capability
from recent_files import RecentFiles

class Kht_Editor(QtGui.QTextEdit):
    def __init__(self, parent=None, fileName=QtCore.QString('')):
        QtGui.QTextEdit.__init__(self,parent)
        init_plugin_system({'plugin_path': './plugins',
                            'plugins': ['autoindent']})
        self.fileName = fileName
        if self.fileName.isEmpty():
            self.fileName = QtCore.QString("Unnamed.txt")
        self.document().setModified(False)

        parent.setWindowTitle(self.fileName)
        #Set kinetic scrollingly 
#        self.kineticScroller = True
        scroller = self.property("kineticScroller").toPyObject()
        scroller.setEnabled(True)
        #scroller.setMode(1)
        #scroller.setDecelerationFactor(0.90)

        #Set no wrap
        self.setLineWrapMode(QtGui.QTextEdit.NoWrap)

        #Remove auto capitalization
        self.setInputMethodHints(Qt.ImhNoAutoUppercase)

    #PySide Bug : The type of e is QEvent instead of QKeyEvent
    def keyPressEvent(self, e):
        if e.type() == QtCore.QEvent.KeyPress:
            for plugin in get_plugins_by_capability('beforeKeyPressEvent'):
                plg = plugin()
                plg.do_beforeKeyPressEvent(self,e)
            QtGui.QTextEdit.keyPressEvent(self, e)
            for plugin in get_plugins_by_capability('afterKeyPressEvent'):
                plg = plugin()
                plg.do_afterKeyPressEvent(self,e)

    def closeEvent(self):
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
            RecentFiles().append(self.fileName)
        except (IOError, OSError), e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception


    def load(self):
        exception = None
        filehandle = None
        try:
            filehandle = QtCore.QFile(self.fileName)
            if not filehandle.open(QtCore.QIODevice.ReadOnly):
                raise IOError, unicode(filehandle.errorString())
            stream = QtCore.QTextStream(filehandle)
            stream.setCodec("UTF-8")
            self.setPlainText(stream.readAll())
            self.document().setModified(False)
            self.setWindowTitle(QtCore.QFileInfo(self.fileName).fileName())
        except (IOError, OSError), error:
            exception = error
        finally:
            if filehandle is not None:
                filehandle.close()
            if exception is not None:
                raise exception

    def isModified(self):
        return self.document().isModified()

    def unIndent(self):
        maincursor = self.textCursor()
        if not maincursor.hasSelection():
            maincursor.movePosition(QtGui.QTextCursor.StartOfBlock)
            line = str(self.document().findBlockByNumber(maincursor\
                                      .blockNumber()).text().toUtf8())
            whitespace = re.match(r"(\s{0,4})", line).group(1)
            for i in range(len(whitespace)): #@UnusedVariable
                maincursor.deleteChar()
        else:
            block = self.document().findBlock(maincursor.selectionStart())
            while True:
                whitespace = re.match(r"(\s{0,4})",
                                str(block.text().toUtf8())).group(1)
                cursor = self.textCursor() 
                cursor.setPosition(block.position())
                for i in range(len(whitespace)): #@UnusedVariable
                    cursor.deleteChar()
                if block.contains(maincursor.selectionEnd()):
                    break
                block = block.next()

    def indent(self):
        maincursor = self.textCursor()
        if not maincursor.hasSelection():
            maincursor.movePosition(QtGui.QTextCursor.StartOfBlock)
            maincursor.insertText("    ")
        else:
            block = self.document().findBlock(maincursor.selectionStart())
            while True:
                cursor = self.textCursor() 
                cursor.setPosition(block.position())
                cursor.insertText("    ")
                if block.contains(maincursor.selectionEnd()):
                    break
                block = block.next()

    def find(self, what, *args):
        print "Find %s %s" % (what, [x for x in args])
        self.document().FindWholeWord(what)

    def comment(self):
        maincursor = self.textCursor()
        if not maincursor.hasSelection():
            maincursor.movePosition(QtGui.QTextCursor.StartOfBlock)
            line = str(self.document().\
                 findBlockByNumber(maincursor.blockNumber()).text().toUtf8())
            if line.startswith('#'):
                maincursor.deleteChar()
            else:
                maincursor.insertText("#")
        else:
            block = self.document().findBlock(maincursor.selectionStart())
            while True:
                cursor = self.textCursor()                                     
                cursor.setPosition(block.position())

                if str(block.text().toUtf8()).startswith('#'):
                    cursor.deleteChar()
                else:
                    cursor.insertText("#")

                if block.contains(maincursor.selectionEnd()):
                    break
                block = block.next()
                
