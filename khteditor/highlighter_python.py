#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Benoît HERVIER
# Licenced under GPLv3


"""KhtEditor a source code editor by Khertan : Python Syntax Hilighter"""

from PySide.QtCore import QRegExp
from PySide.QtGui import QSyntaxHighlighter, \
                         QTextBlockUserData

import keyword

from styles import STYLES

class BracketsInfo:

    def __init__(self, character, position):
        self.character = character
        self.position = position


class TextBlockData(QTextBlockUserData):

    def __init__(self, parent=None):
        super(TextBlockData, self).__init__()
        self.braces = []
        self.valid = False

    def insert_brackets_info(self, info):
        self.valid = True
        self.braces.append(info)

    def isValid(self):
        return self.valid

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

    keywords = keyword.kwlist
    datatype = [ bkey for bkey, bvalue in \
                 __builtins__.items() \
                 if bvalue.__class__ == type ]
    specials = [ bkey for bkey, bvalue in \
                __builtins__.items() \
                if bvalue.__class__ != type ]

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

    def __init__(self, document, styleName = None):
        super(Highlighter, self).__init__(document)

        if styleName in STYLES:
            self.styles = STYLES[styleName]
        else:
            self.styles = STYLES['default']

        #Init error object
#        print type(self.document())
        self.doc = self.document()

        # Multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward
        self.tri_double = ( QRegExp(r'''"""(?!')'''), 2, self.styles['string2'])
        self.tri_single = ( QRegExp(r"""'''(?!")"""), 1, self.styles['string2'])

        #Brace rule
        self.braces = QRegExp('(\{|\}|\(|\)|\[|\])')

        rules = []
        rules += [(r'\b%s\b' % w, 0, self.styles['keyword']) for w in Highlighter.keywords]
        rules += [(r'\b%s\b' % w, 0, self.styles['preprocessor']) for w in Highlighter.preprocessors]
        rules += [(r'\b%s\b' % w, 0, self.styles['datatype']) for w in Highlighter.datatype]
        rules += [(r'\b%s\b' % w, 0, self.styles['special']) for w in Highlighter.specials]
        rules += [(r'%s' % o, 0, self.styles['operator']) for o in Highlighter.operators]
        rules += [(r'%s' % b, 0, self.styles['brace']) for b in Highlighter.braces]

        rules += [
                # Framework PyQt
                (r'\bPyQt4\b|\bPySide\b|\bQt?[A-Z][a-z]\w+\b',0,self.styles['framework']),
                # 'def' followed by an identifier
                (r'\bdef\b\s*(\w+)', 1, self.styles['defclass']),
                # 'class' followed by an identifier
                (r'\bclass\b\s*(\w+)', 1, self.styles['defclass']),
                # Double-quoted string, possibly containing escape sequences
                #(r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
                (r"""(:?"["]".*"["]"|'''.*''')""", 0, self.styles['string']),
                # Single-quoted string, possibly containing escape sequences
                #(r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),
                (r"""(?:'[^']*'|"[^"]*")""", 0, self.styles['string']),
                # From '#' until a newline
                (r'#[^\n]*', 0, self.styles['comment']),
        ]

        # Build a QRegExp for each pattern
        self.rules = [( QRegExp(pat), index, fmt) for (pat, index, fmt) in rules]
        self.rules[-2][0].setMinimal(True)
        self.rules[-3][0].setMinimal(True)


    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        braces = self.braces
        block_data = TextBlockData()

        # Brackets
        index = braces.indexIn(text, 0)

        while index >= 0:
            matched_brace = str(braces.capturedTexts()[0])
            info = BracketsInfo(matched_brace, index)
            block_data.insert_brackets_info(info)
            index = braces.indexIn(text, index + 1)

        self.setCurrentBlockUserData(block_data)

        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        # Do errors coloration
        if hasattr(self.doc,'errors'):
            if self.currentBlock().firstLineNumber() in self.doc.errors:
                self.setFormat(0, self.currentBlock().length(), self.styles['error'])

        self.setCurrentBlockState(0)

        # Do multi-line strings
        self.match_multiline(text, *self.tri_single)
        self.match_multiline(text, *self.tri_double)

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
