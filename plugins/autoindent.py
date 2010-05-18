from PySide.QtGui import QTextEdit
from PySide.QtCore import Qt
from plugins import Plugin
import re

class AutoIndent_Plugin(Plugin):
    capabilities = ['afterKeyPressEvent']

    def do_afterKeyPressEvent(self, widget,event):
        if (event.key() == Qt.Key_Return) or (event.key() == Qt.Key_Enter):
            # copy whitespace from the beginning of the previous line
            cursor = widget.textCursor()
            block = widget.document().findBlockByNumber(cursor.blockNumber()-1)
            whitespace = re.match(r"(\s*)", str(block.text().toUtf8())).group(1)
#            event.ignore()
#            QTextEdit.keyPressEvent(widget, event)
            cursor = widget.textCursor()
            format = cursor.blockFormat()
            format.clearBackground()
            cursor.setBlockFormat(format)
            cursor.insertText(whitespace)
#            print 'marche pas'
