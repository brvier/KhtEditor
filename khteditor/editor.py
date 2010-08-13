#!/usr/bin/env python

"""KhtEditor a source code editor by Khertan : Code Editor"""

import re
from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import Qt
from plugins_api import init_plugin_system, get_plugins_by_capability
from recent_files import RecentFiles

class KhtTextEdit(QtGui.QTextEdit):
    """ Widget which handle all specifities of implemented in the editor"""

    def __init__(self, parent=None, filename=QtCore.QString('')):
        """Initialization, can accept a filepath as argument"""
        QtGui.QTextEdit.__init__(self, parent)
        self.connect(self, QtCore.SIGNAL('cursorPositionChanged()'),  self.highlightCurrentLine);

        #Plugin init move to editor_window.py
        #initialization init of plugin system
        #Maybe be not the best place to do it ...
        #init_plugin_system({'plugin_path': '/home/opt/khteditor/plugins',
        #                    'plugins': ['autoindent']})

        #If we have a filename
        self.filename = filename
        if self.filename.isEmpty():
            self.filename = QtCore.QString("Unnamed.txt")
        self.document().setModified(False)
        parent.setWindowTitle(self.filename)

        #Maemo Finger Kinetic Scrolling
        scroller = self.property("kineticScroller").toPyObject()
        scroller.setEnabled(True)

        #Set no wrap
        self.setLineWrapMode(QtGui.QTextEdit.NoWrap)

        #Remove auto capitalization
        self.setInputMethodHints(Qt.ImhNoAutoUppercase)

        #Keep threaded plugins references to avoid them to be garbage collected
        self.threaded_plugins = []

    #PySide Bug : The type of e is QEvent instead of QKeyEvent
    def keyPressEvent(self, event):
        """Intercept the key event to lets plugin do something if they want"""
        if event.type() == QtCore.QEvent.KeyPress:
            for plugin in get_plugins_by_capability('beforeKeyPressEvent'):
                plg = plugin()
                plg.do_beforeKeyPressEvent(self,event)
            QtGui.QTextEdit.keyPressEvent(self, event)
            for plugin in get_plugins_by_capability('afterKeyPressEvent'):
                plg = plugin()
                plg.do_afterKeyPressEvent(self,event)

    def closeEvent(self):
        """Catch the close event and ask to save if document is modified"""
        if self.document().isModified() and \
           QtGui.QMessageBox.question(self,
                   "Text Editor - Unsaved Changes",
                   "Save unsaved changes in %s?" % self.filename,
                   QtGui.QMessageBox.Yes|QtGui.QMessageBox.No) == \
                QtGui.QMessageBox.Yes:
            try:
                self.save()
            except (IOError, OSError), ioError:
                QtGui.QMessageBox.warning(self, "Text Editor -- Save Error",
                        "Failed to save %s: %s" % (self.filename, ioError))

    def save(self):
        """Hum ... just save ..."""
        if self.filename.startsWith("Unnamed"):
            filename = QtGui.QFileDialog.getSaveFileName(self,
                            "Text Editor -- Save File As",
                            self.filename, "Text files (*.py *.*)")
            if filename.isEmpty():
                return
            self.filename = filename
        self.setWindowTitle(QtCore.QFileInfo(self.filename).fileName())
        exception = None
        filehandle = None
        try:
            #Before FileSave plugin hook
            for plugin in get_plugins_by_capability('beforeFileSave'):
                plg = plugin()
                self.threaded_plugins.append(plg)
                plg.do_beforeFileSave(self)

            filehandle = QtCore.QFile(self.filename)
            if not filehandle.open(QtCore.QIODevice.WriteOnly):
                raise IOError, unicode(filehandle.errorString())
            stream = QtCore.QTextStream(filehandle)
            stream.setCodec("UTF-8")
            stream << self.toPlainText()
            self.document().setModified(False)
            RecentFiles().append(self.filename)
        except (IOError, OSError), ioError:
            exception = ioError
        finally:
            if filehandle is not None:
                filehandle.close()
                for plugin in get_plugins_by_capability('afterFileSave'):
                    plg = plugin()
                    self.threaded_plugins.append(plg)
                    plg.do_afterFileSave(self)

            if exception is not None:
                raise exception

    def highlightCurrentLine(self):
        #Hilgight background
        _color = QtGui.QColor('lightblue').lighter(120)
        _selection = QtGui.QTextEdit.ExtraSelection()
        _selection.format.setBackground(_color)
        _selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
        _selection.cursor = self.textCursor()
        _selection.cursor.clearSelection()
        extraSelection = []
        extraSelection.append(_selection)
        self.setExtraSelections(extraSelection)

#    def hilighterror(self,type,line,comment):
#        print type,line,comment
#        _color = QtGui.QColor()
#        _color.setNamedColor('red')
#        _format = QtGui.QTextCharFormat()
#        _format.setBackground(_color)
#        _format.setFontItalic(True)

        #Hilgight background
#        _color = QtGui.QColor()
#        _color.setNamedColor('red')
#        _color.lighter(160)
#        _selection = QtGui.QTextEdit.ExtraSelection()
#        _selection.format.setBackground(_color)
#        _selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, true)
#
#        _selection.cursor = textCursor()
#        block = self.document().findBlockByLineNumber(line-1)
#        _selection.cursor.cursor.setPosition(block.position())
#        _selection.cursor.clearSelection()
#        self.extraSelections.append(_selection)
#
#Version text add
#        block = self.document().findBlockByLineNumber(line-1)
#        if not (block.text().startsWith('FIXME:')):
#            block = self.document().findBlockByLineNumber(line)
#            cursor = self.textCursor()
#            cursor.setPosition(block.position())
#            cursor.insertText("FIXME:"+type+':'+str(line)+':'+comment+'\n')

#        block.setUnderlineColor(_color)
#        block.setFontItalic(True)

    def load(self):
        """Load ?"""
        exception = None
        filehandle = None
        try:
            filehandle = QtCore.QFile(self.filename)
            if not filehandle.open(QtCore.QIODevice.ReadOnly):
                raise IOError, unicode(filehandle.errorString())
            stream = QtCore.QTextStream(filehandle)
            stream.setCodec("UTF-8")
            self.setPlainText(stream.readAll())
            self.document().setModified(False)
            self.setWindowTitle(QtCore.QFileInfo(self.filename).fileName())
        except (IOError, OSError), error:
            exception = error
        finally:
            if filehandle is not None:
                filehandle.close()
            if exception is not None:
                raise exception

    def isModified(self):
        """Return True if the document is modified"""
        return self.document().isModified()

    def unindent(self):
        """UnIndent the current selection or line"""
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
        """Indent the current selection or line"""
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

    def replace_all(self, what, new, *args):
        """Replace all occurence of a search
        arg[0] -> QtGui.QTextDocument.FindCaseSensitively
        arg[1] -> QtGui.QTextDocument.FindWholeWords
        arg[2] -> QtGui.QTextDocument.FindBackward
        arg[3] -> QtGui.QTextDocument.RegEx
        """
        # Use flags for case match
        flags = QtGui.QTextDocument.FindFlags()
        if args[0]:
            flags = flags|QtGui.QTextDocument.FindCaseSensitively
        if args[1]:
            flags = flags|QtGui.QTextDocument.FindWholeWords
        if args[2]:
            flags = flags|QtGui.QTextDocument.FindBackward

        # Beginning of undo block
        pcursor = self.textCursor()
        pcursor.beginEditBlock()

        #cursor at start as we replace from start
        cursor = self.textCursor()
        cursor.setPosition(0)

        # Replace all we can
        while True:
            # self is the QTextEdit
            if args[3]:
                cursor=self.document().find(QtCore.QRegExp(what),
                                       cursor,flags)
            else:
                cursor=self.document().find(what,cursor,flags)
            if not cursor.isNull():
                if cursor.hasSelection():
                    cursor.insertText(new)
                    print 'insertText %s' % (new,)
                else:
                    print 'no selection'
            else:
                break

        # Mark end of undo block
        pcursor.endEditBlock()

    def replace(self, what, new, *args):
        """Replace the first occurence of a search
        arg[0] -> QtGui.QTextDocument.FindCaseSensitively
        arg[1] -> QtGui.QTextDocument.FindWholeWords
        arg[2] -> QtGui.QTextDocument.FindBackward
        arg[3] -> QtGui.QTextDocument.RegEx
        """
        # Use flags for case match
        flags = QtGui.QTextDocument.FindFlags()
        if args[0]:
            flags = flags|QtGui.QTextDocument.FindCaseSensitively
        if args[1]:
            flags = flags|QtGui.QTextDocument.FindWholeWords
        if args[2]:
            flags = flags|QtGui.QTextDocument.FindBackward

        # Beginning of undo block
        pcursor = self.textCursor()
        pcursor.beginEditBlock()

        # Replace
        # self is the QTextEdit
        if args[3]:
            cursor = self.document().find(QtCore.QRegExp(what),
                                    self.textCursor(), flags)
        else:
            cursor = self.document().find(what, self.textCursor(), flags)
        if not cursor.isNull():
            if cursor.hasSelection():
                cursor.insertText(new)

        # Mark end of undo block
        pcursor.endEditBlock()

    def find(self, what, *args):
        """Perform a search
        arg[0] -> QtGui.QTextDocument.FindCaseSensitively
        arg[1] -> QtGui.QTextDocument.FindWholeWords
        arg[2] -> QtGui.QTextDocument.FindBackward
        arg[3] -> QtGui.QTextDocument.RegEx
        """
        # Use flags for case match
        flags = QtGui.QTextDocument.FindFlags()
        if args[0]:
            flags = flags|QtGui.QTextDocument.FindCaseSensitively
        if args[1]:
            flags = flags|QtGui.QTextDocument.FindWholeWords
        if args[2]:
            flags = flags|QtGui.QTextDocument.FindBackward

        if args[3]:
            cursor = self.document().find(QtCore.QRegExp(what),
                                        self.textCursor(), flags)
        else:
            cursor = self.document().find(what, self.textCursor(), flags)

        if not cursor.isNull():
            self.setTextCursor(cursor)

    def duplicate(self):
        """Duplicate the current line or selection"""
        maincursor = self.textCursor()
        if not maincursor.hasSelection():
            maincursor.movePosition(QtGui.QTextCursor.StartOfBlock)
            line = str(self.document().\
                 findBlockByNumber(maincursor.blockNumber()).text().toUtf8())
            maincursor.movePosition(QtGui.QTextCursor.EndOfBlock)
            maincursor.insertText('\n'+line)
        else:
            block = self.document().findBlock(maincursor.selectionStart())
            line = QtCore.QString()
            while True:
                cursor = self.textCursor()
                cursor.setPosition(block.position())

                line = line + '\n' + block.text()

                if block.contains(maincursor.selectionEnd()):
                    break
                block = block.next()
            cursor.movePosition(QtGui.QTextCursor.EndOfBlock)
            cursor.insertText(line)

    def comment(self):
        """Comment the current line or selection"""
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

