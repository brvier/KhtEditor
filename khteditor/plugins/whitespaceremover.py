from PyQt4.QtGui import QTextEdit,QTextCursor
from PyQt4.QtCore import Qt,SIGNAL
from plugins_api import Plugin
import os
import re

class EndWhiteSpaceRemover(Plugin):
    capabilities = ['afterKeyPressEvent', 'beforeFileSave']
    __version__ = '0.2'

    def do_afterKeyPressEvent(self, widget,event):
        if (event.key() == Qt.Key_Return) or (event.key() == Qt.Key_Enter):
            # delete whitespace at end of the previous line
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
        pos = cursor.position()
        new_text = u''
        linesep = os.linesep
        for line in widget.toPlainText().splitlines():
            new_text += '%s%s' % (unicode.rstrip(line,' \t'),linesep)
        widget.document().setPlainText(new_text)
        cursor = widget.textCursor()
        cursor.setPosition(pos)
        widget.setTextCursor(cursor)
        widget.document().setModified(False)
        widget.document().emit(SIGNAL('modificationChanged(bool)'),False)
