#!/usr/bin/env python

"""KhtEditor a source code editor by Khertan : Python Syntax Hilighter"""

import sys
import re
from PyQt4 import QtCore, QtGui

class Highlighter( QSyntaxHighlighter):

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
        'self',
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

    def __init__(self, document):
        super(Highlighter, self).__init__(document)
        STYLES = {
        'preprocessor': self.format('darkMagenta'),
        'keyword': self.format('darkOrange'),
        'special': self.format('darkMagenta'),
        'operator': self.format('darkMagenta'),
        'brace': self.format('darkGray'),
        'defclass': self.format('blue'),
        'string': self.format('green'),
        'string2': self.format('green'),
        'comment': self.format('red'),
        'framework': self.format('blue'),
        }

        # Multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward
        self.tri_double = ( QRegExp(r'''"""(?!')'''), 2, STYLES['string2'])
        self.tri_single = ( QRegExp(r"""'''(?!")"""), 1, STYLES['string2'])

        rules = []
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword']) for w in Highlighter.keywords]
        rules += [(r'\b%s\b' % w, 0, STYLES['preprocessor']) for w in Highlighter.preprocessors]
        rules += [(r'\b%s\b' % w, 0, STYLES['special']) for w in Highlighter.specials]
        rules += [(r'%s' % o, 0, STYLES['operator']) for o in Highlighter.operators]
        rules += [(r'%s' % b, 0, STYLES['brace']) for b in Highlighter.braces]

        rules += [
                # Framework PyQt
                (r'\bPyQt4\b|\bQt?[A-Z][a-z]\w+\b',0,STYLES['framework']), 
                # 'def' followed by an identifier
                (r'\bdef\b\s*(\w+)', 1, STYLES['defclass']),
                # 'class' followed by an identifier
                (r'\bclass\b\s*(\w+)', 1, STYLES['defclass']),
                # Double-quoted string, possibly containing escape sequences
                #(r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
                (r"""(:?"["]".*"["]"|'''.*''')""", 0, STYLES['string']),
                # Single-quoted string, possibly containing escape sequences
                #(r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),
                (r"""(?:'[^']*'|"[^"]*")""", 0, STYLES['string']),
                # From '#' until a newline
                (r'#[^\n]*', 0, STYLES['comment']),
        ]

        # Build a QRegExp for each pattern
        self.rules = [( QRegExp(pat), index, fmt) for (pat, index, fmt) in rules]
        self.rules[-2][0].setMinimal(True)
        self.rules[-3][0].setMinimal(True)
                
    def format(self,color, style=''):
        """Return a QTextCharFormat with the given attributes.
        """
        _color =  QColor()
        _color.setNamedColor(color)

        _format =  QTextCharFormat()
        _format.setForeground(_color)
        if 'bold' in style:
            _format.setFontWeight(QFont.Bold)
        if 'italic' in style:
            _format.setFontItalic(True)

        return _format
        
    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """        
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)                
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)
            
        # Do multi-line strings
        self.match_multiline(text, *self.tri_single)
        self.match_multiline(text, *self.tri_double)
            
        # QApplication.flush()
        # QApplication.processEvents( QEventLoop.ExcludeUserInputEvents)
        # QApplication.sendPostedEvents()

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
                length = len(text )- start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False