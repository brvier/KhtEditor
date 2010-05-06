#!/usr/bin/env python

"""KhtEditor a source code editor by Khertan : Editor Window"""

import sys
import re
from PyQt4 import QtCore, QtGui
from plugins import init_plugin_system, get_plugins_by_capability

class Window(QtGui.QMainWindow):
    def __init__(self, parent=None,main=None):
        super(Window, self).__init__(parent)
        self.resize(800, 480)
        #self.setupHelpMenu()
        #self.setupFileMenu()
        self.setupEditor()
        self.main = main
        self.main.window_list.append(self)

        self.setCentralWidget(self.editor)
#        self.layout = QtGui.QVBoxLayout()
#        self.setLayout(self.layout)

        self.setWindowTitle(self.tr("Syntax Highlighter"))

    def about(self):
        QtGui.QMessageBox.about(self, self.tr("About Syntax Highlighter"),
                self.tr("<p>The <b>Syntax Highlighter</b> example shows how "
                        "to perform simple syntax highlighting by subclassing "
                        "the QSyntaxHighlighter class and describing "
                        "highlighting rules using regular expressions.</p>"))

    def newFile(self):
        self.editor.clear()

    def openFile(self, fileName):
          inFile = QtCore.QFile(fileName)
          if inFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
              self.editor.setPlainText(QtCore.QString(inFile.readAll()))

    def openFileDialog(self, path=QtCore.QString()):
        fileName = QtCore.QString(path)

        if fileName.isNull():
            fileName = QtGui.QFileDialog.getOpenFileName(self,
                    self.tr("Open File"), "", "C++ Files (*.cpp *.h *.py)")

        if not fileName.isEmpty():
            self.openFileDialog(fileName)

    def setupEditor(self):
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(12)

        self.editor = Kht_Editor()
        #self.editor = QtGui.QTextEdit()
        self.editor.setFont(font)
        self.setupToolBar()
        self.highlighter = Python_Highlighter(self.editor.document())

    def setupToolBar(self):
        self.toolbar = self.addToolBar('Toolbar')
        self.tb_indent = QtGui.QAction(QtGui.QIcon('icons/tb_indent.png'), 'Indent', self)
        self.tb_indent.setShortcut('Ctrl+U')
        self.connect(self.toolbar, QtCore.SIGNAL('triggered()'), self.do_indent)
        self.toolbar.addAction(self.tb_indent)
        self.tb_unindent = QtGui.QAction(QtGui.QIcon('icons/tb_unindent.png'), 'Unindent', self)
        self.tb_unindent.setShortcut('Ctrl+I')
        self.connect(self.toolbar, QtCore.SIGNAL('triggered()'), self.do_unindent)
        self.toolbar.addAction(self.tb_unindent)



    def setupFileMenu(self):
        fileMenu = QtGui.QMenu(self.tr("&File"), self)
        self.menuBar().addMenu(fileMenu)

        fileMenu.addAction(self.tr("&New..."), self.newFile,
                QtGui.QKeySequence(self.tr("Ctrl+N", "File|New")))
        fileMenu.addAction(self.tr("&Open..."), self.openFile,
                QtGui.QKeySequence(self.tr("Ctrl+O", "File|Open")))
        fileMenu.addAction(self.tr("E&xit"), QtGui.qApp.quit,
                QtGui.QKeySequence(self.tr("Ctrl+Q", "File|Exit")))

    def setupHelpMenu(self):
        helpMenu = QtGui.QMenu(self.tr("&Help"), self)
        self.menuBar().addMenu(helpMenu)

        helpMenu.addAction(self.tr("&About"), self.about)
        helpMenu.addAction(self.tr("About &Qt"), QtGui.qApp.aboutQt)

    def do_indent(self):
        print "do_indent"
    def do_unindent(self):
        print "do_unindent"

class Kht_Editor(QtGui.QTextEdit):
    def __init__(self, parent=None):
        QtGui.QTextEdit.__init__(self)
        init_plugin_system({'plugin_path': './plugins', 'plugins': ['autoindent']})


    def keyPressEvent(self, e):
        for plugin in get_plugins_by_capability('beforeKeyPressEvent'):
            plg = plugin()
            plg.do_beforeKeyPressEvent(self,e)
        QtGui.QTextEdit.keyPressEvent(self, e)
        for plugin in get_plugins_by_capability('afterKeyPressEvent'):
            plg = plugin()
            plg.do_afterKeyPressEvent(self,e)

#        if key == QtCore.Qt.Key_Tab:
#            # indent, either current line only or all selected lines
#            maincursor = self.textCursor()
#            if not maincursor.hasSelection():
#                maincursor.insertText("    ")
#            else:
#                block = self.document().findBlock(maincursor.selectionStart())
#                while True:
#                    cursor = self.textCursor()
#                    cursor.setPosition(block.position())
#                    cursor.insertText("    ")
#                    if block.contains(maincursor.selectionEnd()):
#                        break
#                    block = block.next()
#            e.accept()

#        elif (key == QtCore.Qt.Key_Return) or (key == QtCore.Qt.Key_Enter):
#            # copy whitespace from the beginning of the previous line
#            cursor = self.textCursor()
#            block = self.document().findBlockByNumber(cursor.blockNumber())
#            whitespace = re.match(r"(\s*)", str(block.text().toUtf8())).group(1)
#            QtGui.QTextEdit.keyPressEvent(self, e)
#            cursor = self.textCursor()
#            format = cursor.blockFormat()
#            format.clearBackground()
#            cursor.setBlockFormat(format)
#            cursor.insertText(whitespace)
#        else:
#            QtGui.QTextEdit.keyPressEvent(self, e)

class Python_Highlighter(QtGui.QSyntaxHighlighter):

    preprocessors = ['import',
        'from',
        'as',
        'False',
        'None',
        'True',
        '__name__',
        '__debug__'
    ]

    keywords = ['and',
        'assert',
        'break',
        'continue',
        'del',
        'elif',
        'else',
        'except',
        'exec',
        'finally',
        'for',
        'global',
        'if',
        'in',
        'is',
        'lambda',
        'not',
        'or',
        'pass',
        'print',
        'raise',
        'try',
        'while',
        'yield',
                'def',
                'class',
                'return',
    ]

    specials = ['ArithmeticError',
        'AssertionError',
        'AttributeError',
        'EnvironmentError',
        'EOFError',
        'Exception',
        'FloatingPointError',
        'ImportError',
        'IndentationError',
        'IndexError',
        'IOError',
        'KeyboardInterrupt',
        'KeyError',
        'LookupError',
        'MemoryError',
        'NameError',
        'NotImplementedError',
        'OSError',
        'OverflowError',
        'ReferenceError',
        'RuntimeError',
        'StandardError',
        'StopIteration',
        'SyntaxError',
        'SystemError',
        'SystemExit',
        'TabError',
        'TypeError',
        'UnboundLocalError',
        'UnicodeDecodeError',
        'UnicodeEncodeError',
        'UnicodeError',
        'UnicodeTranslateError',
        'ValueError',
        'WindowsError',
        'ZeroDivisionError',

        'Warning',
        'UserWarning',
        'DeprecationWarning',
        'PendingDeprecationWarning',
        'SyntaxWarning',
        'OverflowWarning',
        'RuntimeWarning',
        'FutureWarning',

        '__import__',
        'abs',
        'apply',
        'basestring',
        'bool',
        'buffer',
        'callable',
        'chr',
        'classmethod',
        'cmp',
        'coerce',
        'compile',
        'complex',
        'delattr',
        'dict',
        'dir',
        'divmod',
        'enumerate',
        'eval',
        'execfile',
        'file',
        'filter',
        'float',
        'getattr',
        'globals',
        'hasattr',
        'hash',
        'hex',
        'id',
        'input',
        'int',
        'intern',
        'isinstance',
        'issubclass',
        'iter',
        'len',
        'list',
        'locals',
        'long',
        'map',
        'max',
        'min',
        'object',
        'oct',
        'open',
        'ord',
        'pow',
        'property',
        'range',
        'raw_input',
        'reduce',
        'reload',
        'repr',
        'round',
        'setattr',
        'slice',
        'staticmethod',
        'str',
        'sum',
        'super',
        'tuple',
        'type',
        'unichr',
        'unicode',
        'vars',
        'xrange',
        'zip',
    ]

    operators = [
                '=',
                 # Comparison
                '==', '!=', '<', '<=', '>', '>=',
                # Arithmetic
                '\+', '-', '\*', '/', '//', '\%', '\*\*',
                # In-place
                '\+=', '-=', '\*=', '/=', '\%=',
                # Bitwise
                '\^', '\|', '\&', '\~', '>>', '<<',
    ]

    # Python braces
    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]

    def format(self,color, style=''):
        """Return a QTextCharFormat with the given attributes.
        """
        _color = QtGui.QColor()
        _color.setNamedColor(color)

        _format = QtGui.QTextCharFormat()
        _format.setForeground(_color)
        if 'bold' in style:
            _format.setFontWeight(QFont.Bold)
        if 'italic' in style:
            _format.setFontItalic(True)

        return _format

    def __init__(self, document):
        #QSyntaxHighlighter.__init__(self, document)
        super(Python_Highlighter, self).__init__(document)
        STYLES = {
        'preprocessor': self.format('darkMagenta'),
        'keyword': self.format('orange'),
        'special': self.format('darkMagenta'),
        'operator': self.format('darkMagenta'),
        'brace': self.format('darkGray'),
        'defclass': self.format('blue'),
        'string': self.format('green'),
        'string2': self.format('green'),
        'comment': self.format('red'),
        }

        # Multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward
        self.tri_single = (QtCore.QRegExp("'''"), 1, STYLES['string2'])
        self.tri_double = (QtCore.QRegExp('"""'), 2, STYLES['string2'])

        rules = []
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword']) for w in Python_Highlighter.keywords]
        rules += [(r'\b%s\b' % w, 0, STYLES['preprocessor']) for w in Python_Highlighter.preprocessors]
        rules += [(r'\b%s\b' % w, 0, STYLES['special']) for w in Python_Highlighter.specials]
        rules += [(r'%s' % o, 0, STYLES['operator']) for o in Python_Highlighter.operators]
        rules += [(r'%s' % b, 0, STYLES['brace']) for b in Python_Highlighter.braces]
        rules += [
                # Double-quoted string, possibly containing escape sequences
                (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
                # Single-quoted string, possibly containing escape sequences
                (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),
                # 'def' followed by an identifier
                (r'\bdef\b\s*(\w+)', 1, STYLES['defclass']),
                # 'class' followed by an identifier
                (r'\bclass\b\s*(\w+)', 1, STYLES['defclass']),
                # From '#' until a newline
                (r'#[^\n]*', 0, STYLES['comment']),
        ]

        # Build a QRegExp for each pattern
        self.rules = [(QtCore.QRegExp(pat), index, fmt) for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = expression.cap(nth).length()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

            self.setCurrentBlockState(0)

            # Do multi-line strings
            in_multiline = self.match_multiline(text, *self.tri_single)
            if not in_multiline:
                in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):
        """Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(text)
            # Move past this match
            add = delimiter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = text.length() - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False
