from PyQt4.QtGui import QTextEdit
from PyQt4.QtCore import Qt
from plugins_api import Plugin
import re

class AutoIndent_Plugin(Plugin):
    capabilities = ['afterKeyPressEvent']

    def do_afterKeyPressEvent(self, widget,event):
        if (event.key() == Qt.Key_Return) or (event.key() == Qt.Key_Enter):
            # copy whitespace from the beginning of the previous line
            cursor = widget.textCursor()
            block = widget.document().findBlockByNumber(cursor.blockNumber()-1)
            whitespace = re.match(r"(\s*)", str(block.text().toUtf8())).group(1)
            print type(block.text().toUtf8()),dir(block.text().toUtf8())
            if block.text().toUtf8().right(1) == ':':
                whitespace = whitespace + '    '
            cursor = widget.textCursor()
            format = cursor.blockFormat()
            format.clearBackground()
            cursor.setBlockFormat(format)
            cursor.insertText(whitespace)
