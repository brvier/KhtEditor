from PyQt4.QtGui import QTextEdit,QTextCursor
from PyQt4.QtCore import Qt,SIGNAL
from plugins_api import Plugin
import os
import re

class WhiteSpaceRemover_Plugin(Plugin):
    #Unactivate on save. Too slow for n900 use
    capabilities = ['afterKeyPressEvent',]#'beforeFileSave']

    def do_afterKeyPressEvent(self, widget,event):
        if (event.key() == Qt.Key_Return) or (event.key() == Qt.Key_Enter):
            # delete whitespace at end of the previous line
            print 'Whitespaceremover after called'
            cursor = widget.textCursor()

            #Do not strip whitespace if there is a selection
            if cursor.hasSelection():
                return                
                
            #keep position
            position = cursor.position()
            
            cursor.beginEditBlock()
            cursor.movePosition(QTextCursor.Up,QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.EndOfLine,QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.WordLeft,QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.EndOfWord,QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.EndOfLine,QTextCursor.KeepAnchor)            
            cursor.removeSelectedText()

            #Restore position
            cursor.setPosition(position,QTextCursor.MoveAnchor)            
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
