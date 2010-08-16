from PyQt4.QtGui import QTextEdit,QTextCursor
from PyQt4.QtCore import Qt,SIGNAL
from khteditor.plugins_api import Plugin
import os
import re

class WhiteSpaceRemover_Plugin(Plugin):
    #Unactivate on save. Too slow for n900 use
    capabilities = ['beforeKeyPressEvent',]#'beforeFileSave']

    def do_beforeKeyPressEvent(self, widget,event):
        if (event.key() == Qt.Key_Return) or (event.key() == Qt.Key_Enter):
            # delete whitespace at end of the previous line
            print 'Whitespaceremover called'
            cursor = widget.textCursor()
            cursor.beginEditBlock()
            cursor.movePosition(QTextCursor.WordLeft,QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.EndOfWord,QTextCursor.MoveAnchor)
            if not cursor.atBlockEnd():
                cursor.movePosition(QTextCursor.NextWord,QTextCursor.KeepAnchor)                
                cursor.removeSelectedText()
            cursor.endEditBlock()
            
    def do_beforeFileSave(self, widget):
        # delete whitespace at end of the previous line
        cursor = widget.textCursor()
        line_number = widget.document().findBlock( cursor.position()).blockNumber()
        cursor.beginEditBlock()
        cursor.select(QTextCursor.Document)
        text = cursor.selectedText()
        new_text = u''
        for line in unicode(text).splitlines():
            new_text += '%s%s' % (unicode.rstrip(line,' \t'),os.linesep)
        widget.document().setPlainText(new_text)
        cursor = widget.textCursor()
        cursor.endEditBlock()
        cursor.setPosition(widget.document().findBlockByLineNumber(line_number).position())
        widget.setTextCursor(cursor)
        widget.document().setModified(False)
        widget.document().emit(SIGNAL('modificationChanged(bool)'),False)
