from PySide.QtGui import QTextEdit,QTextCursor
from PySide.QtCore import Qt, \
                         QObject, \
                         Slot
from plugins_api import Plugin
import os
#import re

class TrailingWhiteSpaceRemover(Plugin, QObject):
    capabilities = ['afterKeyPressEvent', 'toolbarHook']
    __version__ = '0.5'

    def __init__(self):
        QObject.__init__(self,parent=None)

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

    def do_toolbarHook(self, widget):
        self.editor_win = widget.parent() #Get the editor_window object
        widget.addAction('Remove trailing white space',self.removeWhiteSpace)

    @Slot()
    def removeWhiteSpace(self):
        # delete whitespace at end of the previous line
        widget = self.editor_win.editor
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
        widget.document().modificationChanged.emit(False)
