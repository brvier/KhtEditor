#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Benoît HERVIER
# Licenced under GPLv3


"""KhtEditor a source code editor by Khertan : Code Editor"""

import re
from PySide.QtCore import Qt, QEvent, \
                        QFileInfo, QSettings, \
                        QFile, QIODevice, \
                        QTextStream, QRegExp, Signal, \
                        QSize, QRect

from PySide.QtGui import QPlainTextEdit, QColor, \
                        QFont,  QFontMetrics, \
                        QTextCursor, QSizePolicy, \
                        QTextCharFormat, QTextEdit, \
                        QTextFormat, QApplication, \
                        QTextDocument, \
                        QPalette

from recent_files import RecentFiles
import os.path
from plugins.plugins_api import filter_plugins_by_capability, \
                                find_plugins

LANGUAGES = ({'Ext':'.R','Name':'r'},
            {'Ext':'.ada','Name':'ada'},
            {'Ext':'.c','Name':'c'},
            {'Ext':'.changelog','Name':'changelog'},
            {'Ext':'.cpp','Name':'cpp'},
            {'Ext':'.csharp','Name':'csharp'},
            {'Ext':'.desktop','Name':'desktop'},
            {'Ext':'.css','Name':'css'},
            {'Ext':'.diff','Name':'diff'},
            {'Ext':'.fort','Name':'fortran'},
            {'Ext':'.gtkrc','Name':'gtkrc'},
            {'Ext':'.haskell','Name':'haskell'},
            {'Ext':'.html','Name':'html'},
            {'Ext':'.idl','Name':'idl'},
            {'Ext':'.ini','Name':'ini'},
            {'Ext':'.java','Name':'java'},
            {'Ext':'.js','Name':'javascript'},
            {'Ext':'.tex','Name':'latex'},
            {'Ext':'.lua','Name':'lua'},
            {'Ext':'makefile','Name':'makefile'},
            {'Ext':'markdown','Name':'markdown'},
            {'Ext':'.msil','Name':'msil'},
            {'Ext':'nemerle','Name':'nemerle'},
            {'Ext':'octave','Name':'octave'},
            {'Ext':'.pas','Name':'pascal'},
            {'Ext':'.pl','Name':'perl'},
            {'Ext':'.php','Name':'php'},
            {'Ext':'.po','Name':'po'},
            {'Ext':('.coffee','.coco'),'Name':'coffeescript', 'Comment':'#'},
            {'Ext':('.py','.pyw'),'Name':'python', 'Exec':'/usr/bin/python -u $1', 'Comment':'#'},
            {'Ext':'.qml','Name':'qml', 'Exec':'cd $0;qmlviewer $1', 'Comment':'//'},
            {'Ext':'.rb','Name':'ruby'},
            {'Ext':'.scheme','Name':'scheme'},
            {'Ext':'.sh','Name':'sh'},
            {'Ext':'.tcl','Name':'tcl'},
            {'Ext':'texinfo','Name':'texinfo'},
            {'Ext':'.txt','Name':'None'},
            {'Ext':'.vb','Name':'vbnet'},
            {'Ext':'verilog','Name':'verilog'},
            {'Ext':'vhdl','Name':'vhdl'},
            {'Ext':'.xml','Name':'xml'},
            )

class KhtTextEditor(QPlainTextEdit):
    """ Widget which handle all specifities of implemented in the editor"""

    showProgress = Signal(bool)
    #filepathChanged = Signal(unicode)
    documentErrorsChanged = Signal()
    sizeChanged = Signal(QSize)
    positionTextChanged = Signal(unicode)
    cursorRectangleChanged = Signal(QRect)

    def __init__(self, parent=None, scroller=None, inQML=False):
        """Initialization, can accept a filepath as argument"""
        QPlainTextEdit.__init__(self, parent)

        # Errors
        self.errors = {}
        self.qt18720 = False
        self.scroller = scroller
        self.inQML = inQML
        self._commentSyntax = None

        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.setTextInteractionFlags(Qt.TextEditable | Qt.TextSelectableByKeyboard)
        if self.inQML:
            self.setVerticalScrollBarPolicy (Qt.ScrollBarAlwaysOff)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        #settings
        self.settings = QSettings()
        self.loadSettings()

        # Brace matching
        self.bracepos = None

        self._filepath = u'Unnamed'

        self.document().setModified(False)

        #Remove auto capitalization
        self.setInputMethodHints(Qt.ImhNoAutoUppercase)

        #Current Line highlight and Bracket matcher
        self.cursorPositionChanged.connect(self.curPositionChanged)
        self.textChanged.connect(self.textEditChanged)
        self.textEditChanged()

        #Enabled Plugin
        if not hasattr(self,'enabled_plugins'):
            #Got the enabled plugin
            settings =  QSettings()
            self.enabled_plugins = []
            for plugin in find_plugins():
                if settings.contains(plugin.__name__):
                    if settings.value(plugin.__name__) == '2':
                        print 'Enable plugin ', plugin
                        self.enabled_plugins.append(plugin())

    def getFilePath(self):
        return self._filepath

    def setFilePath(self, filepath):
        if filepath != self._filepath:
            if self.detectLanguage(filepath) != self.detectLanguage(self._filepath):
                self._filepath = filepath
#                self.load()
                #self.loadHighlighter()
            self._filepath = filepath
            #self.filepathChanged.emit(filepath)

    def loadSettings(self):
        from styles import STYLES

        styleName = self.settings.value('theme')
        if styleName in STYLES:
            style = STYLES[styleName]
        else:
            style = STYLES['default']

        palette = self.palette()
        palette.setColor(QPalette.Base, style['background'].foreground().color())
        palette.setColor(QPalette.Text, style['default'].foreground().color())
        self.setPalette(palette)
#        self.setWindowOpacity(0.9)

        self.hl_color =  style['linehighlight'].foreground().color() #QColor('lightblue').lighter(120)

        if ((self.settings.value("qt18720"))=='2'):
            self.qt18720 = True
        else:
            self.qt18720 = False

        #Set no wrap
        if (self.settings.value("WrapLine") != '2' ):
            self.setLineWrapMode(QPlainTextEdit.NoWrap)
        else:
            self.setLineWrapMode(QPlainTextEdit.WidgetWidth)
            print 'Word wrap enabled'

        font =  QFont()
        try:
            if self.settings.contains('FontName'):
                font.setFamily(self.settings.value('FontName'))
            else:
                font.setFamily("Courier")
        except:
            font.setFamily("Courier")

        #Get Font Size
        try:
            if self.settings.contains('FontSize'):
                font.setPointSize(int(self.settings.value('FontSize')))
            else:
                font.setPointSize(11)
        except:
            font.setPointSize(11)

        #Set Font
        self.fmetrics = QFontMetrics(font)
        self.document().setDefaultFont(font)

    def detectLanguage(self, filepath=None):
        if not filepath: filepath = self._filepath
        ext = os.path.splitext(filepath)[1]
        for lang in LANGUAGES:
            if ext in lang['Ext']:
                return lang['Name']
        return None

    def detectComment(self, filepath=None):
        if not filepath: filepath = self._filepath
        ext = os.path.splitext(filepath)[1]
        for lang in LANGUAGES:
            if ext in lang['Ext']:
                if 'Comment' in lang:
                    return lang['Comment']
                else:
                    return '//'
        return None

    def loadHighlighter(self,filename=None):
        filename = self._filepath
        language = self.detectLanguage(filename)

        print 'Detected Language: ',language
        #Return None if language not yet implemented natively in KhtEditor
        if language == 'python':
            self.showProgress.emit(True)
            QApplication.processEvents()
            from highlighter_python import Highlighter
            self.highlighter = Highlighter(self.document(), styleName=self.settings.value('theme'))
            QApplication.processEvents()
            self.showProgress.emit(False)
        elif (language != None) and (language != 'None'):
            self.showProgress.emit(True)
            QApplication.processEvents()
            from highlighter_generic import Highlighter
            self.highlighter = Highlighter(self.document(),language, styleName=self.settings.value('theme'))
            QApplication.processEvents()
            self.showProgress.emit(False)
        else:
            self.showProgress.emit(True)
            QApplication.processEvents()
            from highlighter_pygments import Highlighter
            self.highlighter = Highlighter(self.document(),
                                                 unicode(filename), styleName=self.settings.value('theme'))
            QApplication.processEvents()
            self.showProgress.emit(False)

    def textEditChanged(self):
        if self.scroller or self.inQML:
            #Resize
            s = self.document().size().toSize()
            s.setHeight((s.height() + 1) * (self.fmetrics.lineSpacing()+1) )
            fr = self.frameRect()
            cr = self.contentsRect()
            self.setMinimumHeight(max(460, s.height() +  (fr.height() - cr.height() - 1)))
            self.setMinimumWidth(max(800,s.width() + (fr.width()-cr.width()) - 1))
            self.sizeChanged.emit(self.size())

    def curPositionChanged(self):
        #Plugin hook
        for plugin in filter_plugins_by_capability('beforeCursorPositionChanged',self.enabled_plugins):
            plugin.do_beforeCursorPositionChanged(self)

        #Hilight current line
        #Workarround QTBUG-18720
        self.highlightCurrentLine()

        #Make sure cursor is visible
        #self.ensureCursorVisible()
        cursor = self.cursorRect()
        cur = self.textCursor()
        pos = cursor.center()
        #self.ensureVisible(pos.x(),pos.y(), 2*cursor.width()+20, 2*cursor.height())
        if self.scroller:
            #self.scroller.ensureVisible(pos.x(),pos.y(),2*cursor.width()+20, 2*cursor.height())
            self.scroller.ensureVisible(pos, 2*cursor.width()+20, 2*cursor.height())
        self.positionTextChanged.emit('%03d-%03d' % (cur.blockNumber()+1, cur.positionInBlock()+1))
        x = pos.x()
        y = pos.y()
        self.cursorRectangleChanged.emit(QRect(x,y,2*cursor.width()+20, 2*cursor.height()))


    def match_left(self, block, character, start, found):
        map = {'{': '}', '(': ')', '[': ']'}
        block_jump = 0

        while block.isValid() and (block_jump < 20):
            data = block.userData()
            if data is not None:
                braces = data.braces
                N = len(braces)

                for k in range(start, N):
                    if braces[k].character == character:
                        found += 1

                    if braces[k].character == map[character]:
                        if not found:
                            return braces[k].position + block.position()
                        else:
                            found -= 1

                block = block.next()
                block_jump += 1
                start = 0

    def match_right(self, block, character, start, found):
        map = {'}': '{', ')': '(', ']': '['}
        block_jump = 0

        while block.isValid() and (block_jump < 20):
            data = block.userData()

            if data is not None:
                braces = data.braces

                if start is None:
                    start = len(braces)
                for k in range(start - 1, -1, -1):
                    if braces[k].character == character:
                        found += 1
                    if braces[k].character == map[character]:
                        if found == 0:
                            return braces[k].position + block.position()
                        else:
                            found -= 1
            block = block.previous()
            block_jump += 1
            start = None

    def check_brackets(self):
        left, right = QTextEdit.ExtraSelection(),\
                      QTextEdit.ExtraSelection()

        cursor = self.textCursor()
        block = cursor.block()
        data = block.userData()
        previous, next = None, None

        if data is not None:
            position = cursor.position()
            block_position = cursor.block().position()
            braces = data.braces
            N = len(braces)

            for k in range(0, N):
                if braces[k].position == position - block_position or\
                   braces[k].position == position - block_position - 1:
                    previous = braces[k].position + block_position
                    if braces[k].character in ['{', '(', '[']:
                        next = self.match_left(block,
                                               braces[k].character,
                                               k + 1, 0)
                    elif braces[k].character in ['}', ')', ']']:
                        next = self.match_right(block,
                                                braces[k].character,
                                                k, 0)

        if (next is not None and next > 0) \
            and (previous is not None and previous > 0):

            format = QTextCharFormat()

            cursor.setPosition(previous)
            cursor.movePosition(QTextCursor.NextCharacter,
                                QTextCursor.KeepAnchor)

            format.setForeground(QColor('blue'))
            format.setBackground(QColor('grey'))
            left.format = format
            left.cursor = cursor

            cursor.setPosition(next)
            cursor.movePosition(QTextCursor.NextCharacter,
                                QTextCursor.KeepAnchor)

            format.setForeground(QColor('blue'))
            format.setBackground(QColor('grey'))
            right.format = format
            right.cursor = cursor

            return left, right

        elif previous is not None:
            format = QTextCharFormat()

            cursor.setPosition(previous)
            cursor.movePosition(QTextCursor.NextCharacter,
                                QTextCursor.KeepAnchor)

            format.setForeground(QColor('red'))
            format.setBackground(QColor('grey'))
            left.format = format
            left.cursor = cursor
            return (left,)
        elif next is not None:
            format = QTextCharFormat()

            cursor.setPosition(next)
            cursor.movePosition(QTextCursor.NextCharacter,
                                QTextCursor.KeepAnchor)

            format.setForeground(QColor('red'))
            format.setBackground(QColor('grey'))
            left.format = format
            left.cursor = cursor
            return (left,)

    #PySide Bug : The type of e is QEvent instead of QKeyEvent
    def keyPressEvent(self, event):
        """Intercept the key event to lets plugin do something if they want"""
        if event.type() ==  QEvent.KeyPress:
            for plugin in filter_plugins_by_capability('beforeKeyPressEvent',self.enabled_plugins):
                plugin.do_beforeKeyPressEvent(self,event)
            QPlainTextEdit.keyPressEvent(self, event)
            for plugin in filter_plugins_by_capability('afterKeyPressEvent',self.enabled_plugins):
                plugin.do_afterKeyPressEvent(self,event)

    def save(self):
        """Hum ... just save ..."""
        exception = None
        filehandle = None
        try:
            #Before FileSave plugin hook
            for plugin in filter_plugins_by_capability('beforeFileSave',self.enabled_plugins):
                plugin.do_beforeFileSave(self)

            filehandle =  QFile(self._filepath)
            if not filehandle.open( QIODevice.WriteOnly):
                raise IOError, unicode(filehandle.errorString())
            stream =  QTextStream(filehandle)
            stream.setCodec("UTF-8")
            stream << self.toPlainText()
            self.document().setModified(False)
            RecentFiles().append(self._filepath)
        except (IOError, OSError), ioError:
            exception = ioError
        finally:
            if filehandle is not None:
                filehandle.close()
                for plugin in filter_plugins_by_capability('afterFileSave',self.enabled_plugins):
                    plugin.do_afterFileSave(self)

            if exception is not None:
                raise exception

    def highlightCurrentLine(self):
        #Hilgight background
        _selection =  QTextEdit.ExtraSelection()
        _selection.cursor = self.textCursor()
        _selection.cursor.clearSelection()
        _selection.format.setBackground(self.hl_color)
        _selection.format.setProperty( QTextFormat.FullWidthSelection, True)
        extraSelection = []
        extraSelection.append(_selection)

        extras = self.check_brackets()
        if extras:
            extraSelection.extend(extras)

        if not self.qt18720:
            self.setExtraSelections(extraSelection)

    def load(self):
        """Load ?"""
        exception = None
        filehandle = None
        try:
            filehandle =  QFile(self._filepath)
            if not filehandle.open( QIODevice.ReadOnly):
                raise IOError, unicode(filehandle.errorString())
            stream =  QTextStream(filehandle)
            stream.setCodec("UTF-8")
            QApplication.processEvents()
            self.setPlainText(stream.readAll())
            self.document().setModified(False)
            self.setWindowTitle( QFileInfo(self._filepath).fileName())
            self.loadHighlighter(self._filepath)
            for plugin in filter_plugins_by_capability('afterFileOpen',self.enabled_plugins):
                plugin.do_afterFileOpen(self)
        except (IOError, OSError), error:
            exception = error
        finally:
            if filehandle is not None:
                filehandle.close()
            if exception is not None:
                raise exception
        self.textChanged.emit()

    def isModified(self):
        """Return True if the document is modified"""
        return self.document().isModified()

    def unindent(self):
        """UnIndent the current selection or line"""
        maincursor = self.textCursor()
        if not maincursor.hasSelection():
            maincursor.movePosition( QTextCursor.StartOfBlock)
            line = str(self.document().findBlockByNumber(maincursor\
                                      .blockNumber()).text())
            whitespace = re.match(r"(\s{0,4})", line).group(1)
            for i in range(len(whitespace)): #@UnusedVariable
                maincursor.deleteChar()
        else:
            block = self.document().findBlock(maincursor.selectionStart())
            while True:
                whitespace = re.match(r"(\s{0,4})",
                                str(block.text())).group(1)
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
            maincursor.movePosition( QTextCursor.StartOfBlock)
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
        arg[0] ->  QTextDocument.FindCaseSensitively
        arg[1] ->  QTextDocument.FindWholeWords
        arg[2] ->  QTextDocument.FindBackward
        arg[3] ->  QTextDocument.RegEx
        """
        # Use flags for case match
        flags =  QTextDocument.FindFlags()
        if args[0]:
            flags = flags| QTextDocument.FindCaseSensitively
        if args[1]:
            flags = flags| QTextDocument.FindWholeWords
        if args[2]:
            flags = flags| QTextDocument.FindBackward

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
                cursor=self.document().find( QRegExp(what),
                                       cursor,flags)
            else:
                cursor=self.document().find(what,cursor,flags)
            if not cursor.isNull():
                if cursor.hasSelection():
                    cursor.insertText(new)
                else:
                    print 'no selection'
            else:
                break

        # Mark end of undo block
        pcursor.endEditBlock()

    def replace(self, what, new, *args):
        """Replace the first occurence of a search
        arg[0] ->  QTextDocument.FindCaseSensitively
        arg[1] ->  QTextDocument.FindWholeWords
        arg[2] ->  QTextDocument.FindBackward
        arg[3] ->  QTextDocument.RegEx
        """
        # Use flags for case match
        flags =  QTextDocument.FindFlags()
        if args[0]:
            flags = flags| QTextDocument.FindCaseSensitively
        if args[1]:
            flags = flags| QTextDocument.FindWholeWords
        if args[2]:
            flags = flags| QTextDocument.FindBackward

        # Beginning of undo block
        pcursor = self.textCursor()
        pcursor.beginEditBlock()

        cursor = self.textCursor()

        # Replace
        # self is the QTextEdit
        if args[3]==True:
            cursor = self.document().find( QRegExp(what),
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
        arg[0] ->  QTextDocument.FindCaseSensitively
        arg[1] ->  QTextDocument.FindWholeWords
        arg[2] ->  QTextDocument.FindBackward
        arg[3] ->  QTextDocument.RegEx
        """
        print 'find called'

        # Use flags for case match
        flags =  QTextDocument.FindFlags()
        if args[0]==True:
            flags = flags |  QTextDocument.FindCaseSensitively
        if args[1]==True:
            flags = flags |  QTextDocument.FindWholeWords
        if args[2]==True:
            flags = flags |  QTextDocument.FindBackward

        cursor = self.textCursor()
        if args[3]==True:
            cursor = self.document().find( QRegExp(what),
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
            maincursor.movePosition( QTextCursor.StartOfBlock)
            line = str(self.document().\
                 findBlockByNumber(maincursor.blockNumber()).text())
            maincursor.movePosition( QTextCursor.EndOfBlock)
            maincursor.insertText('\n'+line)
        else:
            block = self.document().findBlock(maincursor.selectionStart())
            line = u''
            while True:
                cursor = self.textCursor()
                cursor.setPosition(block.position())

                line = line + '\n' + block.text()

                if block.contains(maincursor.selectionEnd()):
                    break
                block = block.next()
            cursor.movePosition( QTextCursor.EndOfBlock)
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
        if not self._commentSyntax:
            self._commentSyntax = self.detectComment()
        _commentSyntax = self._commentSyntax

        maincursor = self.textCursor()
        if not maincursor.hasSelection():
            maincursor.movePosition( QTextCursor.StartOfBlock)
            line = str(self.document().\
                 findBlockByNumber(maincursor.blockNumber()).text())
            if line.startswith(_commentSyntax):
                for index in range(len(_commentSyntax)):
                    maincursor.deleteChar()
            else:
                maincursor.insertText(_commentSyntax)
        else:
            block = self.document().findBlock(maincursor.selectionStart())
            while True:
                cursor = self.textCursor()
                cursor.setPosition(block.position())

                if str(block.text()).startswith(_commentSyntax):
                    for index in range(len(_commentSyntax)):
                        cursor.deleteChar()
                else:
                    cursor.insertText(_commentSyntax)

                if block.contains(maincursor.selectionEnd()):
                    break
                block = block.next()

    def __select_text(self, position_from, position_to):
        position_from = self.get_position(position_from)
        position_to = self.get_position(position_to)
        cursor = self.textCursor()
        cursor.setPosition(position_from)
        cursor.setPosition(position_to,  QTextCursor.KeepAnchor)
        return cursor


    def get_position(self, position):
        cursor = self.textCursor()
        if position == 'cursor':
            pass
        elif position == 'sob':
            cursor.movePosition( QTextCursor.Start)
        elif position == 'sol':
            cursor.movePosition( QTextCursor.StartOfBlock)
        elif position == 'eol':
            cursor.movePosition( QTextCursor.EndOfBlock)
        elif position == 'eof':
            cursor.movePosition( QTextCursor.End)
        elif position == 'sof':
            cursor.movePosition( QTextCursor.Start)
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

        return unicode(text)

    def getExecuteCommand(self):
        ext = os.path.splitext(self._filepath)[1]
        for lang in LANGUAGES:
            if ext in lang['Ext']:
                command = lang['Exec'].replace('$0', os.path.dirname(self._filepath))
                return command.replace('$1', os.path.basename(self._filepath))
        return None