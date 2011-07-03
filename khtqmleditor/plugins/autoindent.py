from PySide.QtGui import QTextEdit
from PySide.QtCore import Qt
from plugins_api import Plugin
import re



class AutoIndent(Plugin):
    capabilities = ['afterKeyPressEvent']
    __version__ = '0.2'
    
    def do_afterKeyPressEvent(self, widget,event):
        if (event.key() == Qt.Key_Return) or (event.key() == Qt.Key_Enter):
            # copy whitespace from the beginning of the previous line
            cursor = widget.textCursor()
            block = widget.document().findBlockByNumber(cursor.blockNumber()-1)
            whitespace = re.match(r"(\s*)", unicode(block.text())).group(1)
            print type(block.text()),dir(block.text())
            if block.text()[-1:] == ':':
                whitespace = whitespace + '    '
            cursor = widget.textCursor()
            format = cursor.blockFormat()
            format.clearBackground()
            cursor.setBlockFormat(format)
            cursor.insertText(whitespace)
