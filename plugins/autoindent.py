from PyQt4.QtGui import QTextEdit
from PyQt4.QtCore import Qt
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
            if block.text().toUtf8().endswith(':'):
                whitespace = whitespace + 4
            cursor = widget.textCursor()
            format = cursor.blockFormat()
            format.clearBackground()
            cursor.setBlockFormat(format)
            cursor.insertText(whitespace)
