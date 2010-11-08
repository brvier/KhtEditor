#!/usr/bin/env python

"""KhtEditor a source code editor by Khertan : Code Editor"""

import re
from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import Qt
from plugins.plugins_api import init_plugin_system, filter_plugins_by_capability
from recent_files import RecentFiles


class KhtTextEdit(QtGui.QPlainTextEdit):
    """ Widget which handle all specifities of implemented in the editor"""
        
    def __init__(self, parent=None, filename=QtCore.QString('')):
        """Initialization, can accept a filepath as argument"""
        QtGui.QPlainTextEdit.__init__(self, parent)
#        self.connect(self, QtCore.SIGNAL('cursorPositionChanged()'),  self.highlightCurrentLine);

        self.hl_color = QtGui.QColor('lightblue').lighter(120)
        # Brace matching
        self.bracepos = None
        # Init scroller
        scroller = None
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
#        scroller = self.property("kineticScroller").toPyObject()
#        print 'Class kineticScrolling',type(scroller),':',dir(scroller)
#        scroller.reset()
#        scroller.setEnabled(True)
#        scroller.setDragInertia(0.85)
#        scroller.setMinimumVelocity(0)
#        scroller.setMaximumVelocity(0.5)
#        scroller.setDecelerationFactor(0.99)
#        scroller.setFastVelocityFactor(0.99)
#        scroller.setMode(1)
#        print scroller.decelerationFactor()
#        print scroller.fastVelocityFactor()
#        print scroller.maximumVelocity()
#        print scroller.minimumVelocity()
#        print scroller.dragInertia()
#        self.setWidgetResizable(True)

        #Set no wrap
        if (parent.settings.value("WrapLine").toBool()):
            self.setLineWrapMode(QtGui.QPlainTextEdit.WidgetWidth)            
        else:
            self.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)

        #Get Font Size
        fontsize = parent.settings.value("FontSize").toInt()[0]
        if fontsize==0:
            fontsize=11
        #Get Font
        try:
            fontname = parent.settings.value("FontName").toString()
        except:
            fontname = 'Monospace'
        #Set Font
        self.document().setDefaultFont(QtGui.QFont(fontname,fontsize))
        

        #Remove auto capitalization
        self.setInputMethodHints(Qt.ImhNoAutoUppercase)
        
        #Keep threaded plugins references to avoid them to be garbage collected
        self.threaded_plugins = []

        self.enabled_plugins = parent.enabled_plugins

        #Current Line highlight and Bracket matcher
        self.cursorPositionChanged.connect(self.curPositionChanged)
        self.textChanged.connect(self.textEditChanged)
        # Brackets ExtraSelection ...

    def textEditChanged(self):
        #Resize
        doc = self.document()
        cursor = self.cursorRect()
        s = doc.size()
        s.setHeight((s.height() + 1) * (self.fontMetrics().lineSpacing() + 1))
        fr = self.frameRect()
        cr = self.contentsRect()
        self.setMinimumHeight(max(s.height(), s.height() + (fr.height() - cr.height() - 1)))
        self.setMinimumWidth(s.width())

    def curPositionChanged(self):
        #Hilight current line
        self.highlightCurrentLine()
        
        #Make sure cursor is visible
        cursor = self.cursorRect()
        pos = self.pos()
        #scroller = self.parentWidget().property("kineticScroller").toPyObject() 
        #pos = self.parent().mapToParent(pos) 
        #print type(self.parent()), type(self.parentWidget()),type(scroller)
        #print pos, pos.x(), pos.y(), (pos + cursor.center()).y()
        #self.scroller.ensureVisible(pos + cursor.center(), 10 + cursor.width(),
        #                       2 * cursor.height())
#        pw = self
        self.scroller.ensureVisible(cursor.center(), 2*cursor.width(), 2*cursor.height())
#        while (pw):
#            if (pw.parentWidget()):
#                area = pw.parentWidget()
#                print area,area.parentWidget(),area.parent()
#                if (type(area) == QtGui.QScrollArea ):
#                    scroller = area.property("kineticScroller").toPyObject()
#                    if (scroller):
#                        print pos.x(),pos.y(),cursor.center().x(),cursor.center().y()
#                        scroller.ensureVisible(cursor.center(), 2*cursor.width(), 2*cursor.height())
#                    break
#            pos = pw.mapToParent(pos)
#            pw = pw.parentWidget()
#
    #PySide Bug : The type of e is QEvent instead of QKeyEvent
    def keyPressEvent(self, event):
        """Intercept the key event to lets plugin do something if they want"""
        if event.type() == QtCore.QEvent.KeyPress:
            for plugin in filter_plugins_by_capability('beforeKeyPressEvent',self.enabled_plugins):
                plg = plugin()
                plg.do_beforeKeyPressEvent(self,event)
            QtGui.QPlainTextEdit.keyPressEvent(self, event)
            for plugin in filter_plugins_by_capability('afterKeyPressEvent',self.enabled_plugins):
                plg = plugin()
                plg.do_afterKeyPressEvent(self,event)

    def closeEvent(self,event):
        """Catch the close event and ask to save if document is modified"""
        answer = self.document().isModified() and \
        QtGui.QMessageBox.question(self,
               "Text Editor - Unsaved Changes",
               "Save unsaved changes in %s?" % self.filename,
               QtGui.QMessageBox.Yes|QtGui.QMessageBox.No|QtGui.QMessageBox.Close)
        if answer == QtGui.QMessageBox.Yes:
            try:
                self.save()
                event.accept()
            except (IOError, OSError), ioError:
                QtGui.QMessageBox.warning(self, "Text Editor -- Save Error",
                        "Failed to save %s: %s" % (self.filename, ioError))
                event.ignore()
        elif answer == QtGui.QMessageBox.Close:
            return event.ignore()
        else:
            return event.accept()

    def save(self):
        """Hum ... just save ..."""
        if self.filename.startsWith("Unnamed"):
            filename = self.parent().saveAsFile()  
            if not filename.isEmpty():            
                return
            self.filename = filename
        self.setWindowTitle(QtCore.QFileInfo(self.filename).fileName())
        exception = None
        filehandle = None
        try:
            #Before FileSave plugin hook
            for plugin in filter_plugins_by_capability('beforeFileSave',self.enabled_plugins):
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
                for plugin in filter_plugins_by_capability('afterFileSave',self.enabled_plugins):
                    plg = plugin()
                    self.threaded_plugins.append(plg)
                    plg.do_afterFileSave(self)

            if exception is not None:
                raise exception

    def __find_brace_match(self, position, brace, forward):
        if forward:
            bracemap = {'(': ')', '[': ']', '{': '}'}
            text = self.get_text(position, 'eof')
            i_start_open = 1
            i_start_close = 1
        else:            
            bracemap = {')': '(', ']': '[', '}': '{'}
            text = self.get_text('sob', position)
            i_start_open = len(text)-1
            i_start_close = len(text)-1

        while True:
            if forward:
                i_close = text.find(bracemap[brace], i_start_close)
            else:
                i_close = text.rfind(bracemap[brace], 0, i_start_close+1)
            if i_close > -1:
                if forward:
                    i_start_close = i_close+1
                    i_open = text.find(brace, i_start_open, i_close)
                else:
                    i_start_close = i_close-1
                    i_open = text.rfind(brace, i_close, i_start_open+1)
                if i_open > -1:
                    if forward:
                        i_start_open = i_open+1
                    else:
                        i_start_open = i_open-1
                else:
                    # found matching brace
                    if forward:
                        return position+i_close
                    else:
                        return position-(len(text)-i_close)
            else:
                # no matching brace
                return
    
    def __highlight(self, positions, color=None, cancel=False):
        cursor = QtGui.QTextCursor(self.document())
        modified = self.document().isModified()
        for position in positions:
            if position > self.get_position('eof'):
                return
            cursor.setPosition(position)
            cursor.movePosition(QtGui.QTextCursor.NextCharacter,
                                QtGui.QTextCursor.KeepAnchor)
            charformat = cursor.charFormat()            
            pen = QtGui.QPen(Qt.NoPen) if cancel else QtGui.QPen(color)
            charformat.setTextOutline(pen)
            cursor.setCharFormat(charformat)
        if cancel:
            charformat = QtGui.QTextCharFormat()
            cursor.movePosition(QtGui.QTextCursor.NextCharacter,
                                QtGui.QTextCursor.KeepAnchor)
            cursor.setCharFormat(charformat)            
            cursor.clearSelection()
            self.setCurrentCharFormat(charformat)
        self.document().setModified(modified)

            
    def highlightCurrentLine(self):            
        #Hilgight background
        _selection = QtGui.QTextEdit.ExtraSelection()
        _selection.format.setBackground(self.hl_color)
        _selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)        
        _selection.cursor = self.textCursor()
        _selection.cursor.clearSelection()
        extraSelection = []
        extraSelection.append(_selection)
#        self.setExtraSelections(extraSelection)

#        cursor = QtGui.QTextCursor(self.document())
#        charformat = cursor.charFormat()            
#        charformat.setTextOutline(QtGui.QPen(Qt.NoPen))            
#        cursor.setCharFormat(charformat)
        
        #Highlight Braces
        if self.bracepos is not None:
#            self.__highlight(self.bracepos, cancel=True)
            print 'should be canceled'
            self.bracepos = None
        cursor = self.textCursor()        
        if cursor.position() == 0:
            self.setExtraSelections(extraSelection)
            return
        cursor.movePosition(QtGui.QTextCursor.PreviousCharacter,
                            QtGui.QTextCursor.KeepAnchor)                           
        text = unicode(cursor.selectedText())
        pos1 = cursor.position()
        if text in (')', ']', '}'):
            pos2 = self.__find_brace_match(pos1, text, forward=False)
        elif text in ('(', '[', '{'):
            pos2 = self.__find_brace_match(pos1, text, forward=True)
        else:
            self.setExtraSelections(extraSelection)
            return
        if pos2 is not None:
            self.bracepos = (pos1, pos2)
#            self.__highlight(self.bracepos, color=Qt.blue)
            print 'Bracket match'
            _selection = QtGui.QTextEdit.ExtraSelection()
            _selection.format.setForeground(Qt.white)
#            _selection.format.setFontWeight(99)
            _selection.format.setBackground(Qt.blue)
            _selection.cursor = cursor
            extraSelection.append(_selection)
            _selection = QtGui.QTextEdit.ExtraSelection()
            _selection.format.setForeground(Qt.white)
            _selection.format.setBackground(Qt.blue)
            _selection.cursor = self.textCursor()
            _selection.cursor.setPosition(pos2)
            _selection.cursor.movePosition(QtGui.QTextCursor.NextCharacter,
                            QtGui.QTextCursor.KeepAnchor)
            extraSelection.append(_selection)
        else:
            self.bracepos = (pos1,)
#            self.__highlight(self.bracepos, color=Qt.red)
            _selection = QtGui.QTextEdit.ExtraSelection()
#            _selection.format.setFontWeight(75)
            _selection.format.setBackground(Qt.red)
            _selection.format.setForeground(Qt.white)
#            _selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)        
            _selection.cursor = cursor
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
            QtGui.QApplication.processEvents()
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

        cursor = self.textCursor()
    
        # Replace
        # self is the QTextEdit
        if args[3]==True:
            cursor = self.document().find(QtCore.QRegExp(what),
                                    cursor, flags)                
        else:
            cursor = self.document().find(what, cursor, flags)
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
        print 'find called'
        
        # Use flags for case match
        flags = QtGui.QTextDocument.FindFlags()
        if args[0]==True:
            flags = flags | QtGui.QTextDocument.FindCaseSensitively
        if args[1]==True:
            flags = flags | QtGui.QTextDocument.FindWholeWords
        if args[2]==True:
            flags = flags | QtGui.QTextDocument.FindBackward

        cursor = self.textCursor()
        if args[3]==True:
            cursor = self.document().find(QtCore.QRegExp(what),
                                       cursor , flags)
        else:
            cursor = self.document().find(what,
                                       cursor, flags)

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
        
    def gotoLine(self, line):
            print 'goto line:'+str(line)
            cursor = self.textCursor()
            block = self.document().findBlockByLineNumber(line-1)
            cursor.setPosition(block.position())
            self.setTextCursor(cursor)
            self.ensureCursorVisible()
            self.parent().activateWindow()
            
            
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

    def __select_text(self, position_from, position_to):
        position_from = self.get_position(position_from)
        position_to = self.get_position(position_to)
        cursor = self.textCursor()
        cursor.setPosition(position_from)
        cursor.setPosition(position_to, QtGui.QTextCursor.KeepAnchor)
        return cursor

        
    def get_position(self, position):
        cursor = self.textCursor()
        if position == 'cursor':
            pass
        elif position == 'sob':
            cursor.movePosition(QtGui.QTextCursor.Start)
        elif position == 'sol':
            cursor.movePosition(QtGui.QTextCursor.StartOfBlock)
        elif position == 'eol':
            cursor.movePosition(QtGui.QTextCursor.EndOfBlock)
        elif position == 'eof':
            cursor.movePosition(QtGui.QTextCursor.End)
        elif position == 'sof':
            cursor.movePosition(QtGui.QTextCursor.Start)
        else:
            # Assuming that input argument was already a position
            return position
        return cursor.position()

    def get_text(self, position_from, position_to):
        """
        Return text between *position_from* and *position_to*
        Positions may be positions or 'sob','sol', 'eol', 'sof', 'eof' or 'cursor'
        """
        cursor = self.__select_text(position_from, position_to)
        text = cursor.selectedText()
#        if not text.isEmpty():
#            while text.endsWith("\n"):
#                text.chop(1)
#            while text.endsWith(u"\u2029"):
#                text.chop(1)
        return unicode(text)