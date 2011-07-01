# -*- coding: utf-8 -*-
import os
import xml.sax
from xml.sax.handler import ContentHandler
from xml.sax.saxutils import unescape

from PySide.QtCore import QRegExp, Qt
from PySide.QtGui import QSyntaxHighlighter, QColor, QTextCharFormat, \
    QTextBlockUserData, QFont

SYNTAX_PATH = [ os.path.join('.', 'syntax'),
                os.path.abspath('.'),
                os.path.abspath(os.path.dirname(__file__)),
                os.path.join(os.path.expanduser('~'),'.khteditor','syntax'),
                '/usr/lib/python2.5/site-packages/khteditor/syntax']


def format(color, style=''):
    """Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format

class XMLSyntaxParser(ContentHandler):
    def __init__(self,lang_name):
        ContentHandler.__init__(self)

        self._grammar = []
        self._comments = []

        # search for syntax-files:
        fname = None
        for syntax_dir in SYNTAX_PATH:
            fname = os.path.join(syntax_dir, "%s.xml"%lang_name)
            if os.path.isfile(fname): break

        if not os.path.isfile(fname):
            raise Exception("No syntax-file for %s found !"%lang_name)

        xml.sax.parse(fname, self)

    def get_style(self,style):
        try:
            return STYLES[style]
        except KeyError, err:
            print 'Unknow style :',err
            return STYLES['default']

    # Dispatch start/end - document/element and chars
    def startDocument(self):
        self.__stack   = []

    def endDocument(self):
        del self.__stack

    def startElement(self, name, attr):
        self.__stack.append( (name, attr) )
        if hasattr(self, "start_%s"%name):
            handler = getattr(self, "start_%s"%name)
            handler(attr)

    def endElement(self, name):
        if hasattr(self, "end_%s"%name):
            handler = getattr(self, "end_%s"%name)
            handler()
        del self.__stack[-1]

    def characters(self, txt):
        if not self.__stack: return
        name, attr = self.__stack[-1]

        if hasattr(self, "chars_%s"%name):
            handler = getattr(self, "chars_%s"%name)
            handler(txt)

    # Handle regexp-patterns
    def start_pattern(self, attr):
        self.__pattern = ""
        self.__group   = 0
        self.__flags   = ''
        self.__style   = attr['style']
        if 'group' in attr.keys(): self.__group = int(attr['group'])
        if 'flags' in attr.keys(): self.__flags = attr['flags']

    def end_pattern(self):
        regexp = QRegExp(self.__pattern)
        if 'I' in self.__flags:
            regexp.setCaseSensitivity(Qt.CaseInsensitive)
        rule = (regexp, 0, self.get_style(self.__style), )
        self._grammar.append(rule)
        del self.__pattern
        del self.__group
        del self.__flags
        del self.__style

    def chars_pattern(self, txt):
        self.__pattern += unescape(txt)

    # handle keyword-lists
    def start_keywordlist(self, attr):
        self.__style = "keyword"
        self.__flags = ""
        if 'style' in attr.keys():
            self.__style = attr['style']
        if 'flags' in attr.keys():
            self.__flags = attr['flags']
        self.__keywords = []

    def end_keywordlist(self):
        rules = [(r'\b%s\b' % w, 0, self.get_style(self.__style)) for w in self.__keywords]
        self._grammar += ([(QRegExp(pat), index, fmt) for (pat, index, fmt) in rules])
        del self.__keywords
        del self.__style
        del self.__flags

    def start_keyword(self, attr):
        self.__keywords.append("")

    def end_keyword(self):
        if not self.__keywords[-1]:
            del self.__keywords[-1]

    def chars_keyword(self, txt):
        parent,pattr = self.__stack[-2]
        if not parent == "keywordlist": return
        self.__keywords[-1] += unescape(txt)

    #handle String-definitions
    def start_string(self, attr):
        self.__style = "string"
        self.__escape = None
        if 'escape' in attr.keys():
            self.__escape = attr['escape']
        if 'style' in attr.keys():
            self.__style = attr['style']
        self.__start_pattern = ""
        self.__end_pattern = ""

    def end_string(self):
        #'[^'\\]*(\\.[^'\\]*)*'
        #regexp = QRegExp('%s[^%s%s]*(%s.[^%s%s]*)*%s'%(self.__start_pattern,self.__start_pattern,self.__escape,self.__escape,self.__end_pattern,self.__escape,self.__end_pattern))
        #'[^'\\]*(?:\\.[^'\\]*)*'
        if self.__escape == '\\':
            self.__escape = '\\\\'
        regexp = QRegExp("%s[^%s%s]*(?:%s.[^%s%s]*)*%s"%(self.__start_pattern,self.__start_pattern,self.__escape,self.__escape,self.__end_pattern,self.__escape,self.__end_pattern))
        print regexp
        # regexp = QRegExp(r'%s[^%s]*%s'%(self.__start_pattern,self.__end_pattern,
                           #self.__escape,
                           # self.__end_pattern))
        strdef = (regexp,0, self.get_style(self.__style))
        self._grammar.append(strdef)
        del self.__style
        del self.__escape
        del self.__start_pattern
        del self.__end_pattern

    #handle Multiline def
    def start_multilines(self, attr):
        self.__style = "comment"
        self.__escape = None
        if 'escape' in attr.keys():
            self.__escape = attr['escape']
        if 'style' in attr.keys():
            self.__style = attr['style']
        self.__start_pattern = ""
        self.__end_pattern = ""

    def end_multilines(self):
        strdef = (QRegExp(self.__start_pattern),QRegExp(self.__end_pattern),0, self.get_style(self.__style))
        self._comments.append(strdef)
        del self.__style
        del self.__escape
        del self.__start_pattern
        del self.__end_pattern

    def chars_starts(self, txt):
        self.__start_pattern += unescape(txt)

    def chars_ends(self, txt):
        self.__end_pattern += unescape(txt)

    # handle style
    def start_style(self, attr):
        self.__style_props = dict()
        self.__style_name = attr['name']

    def end_style(self):
        self._styles[self.__style_name] = self.__style_props
        del self.__style_props
        del self.__style_name

    def start_property(self, attr):
        self.__style_prop_name = attr['name']

    def chars_property(self, value):
        value.strip()

        # convert value
        if self.__style_prop_name in ['font','foreground','background',]:
            pass

        elif self.__style_prop_name == 'variant':
            if not value in self.style_variant_table.keys():
                Exception("Unknown style-variant: %s"%value)
            value = self.style_variant_table[value]

        elif self.__style_prop_name == 'underline':
            if not value in self.style_underline_table.keys():
                Exception("Unknown underline-style: %s"%value)
            value = self.style_underline_table[value]

        elif self.__style_prop_name == 'scale':
            if not value in self.style_scale_table.keys():
                Exception("Unknown scale-style: %s"%value)
            value = self.style_scale_table[value]

        elif self.__style_prop_name == 'weight':
            if not value in self.style_weight_table.keys():
                Exception("Unknown style-weight: %s"%value)
            value = self.style_weight_table[value]

        elif self.__style_prop_name == 'style':
            if not value in self.style_style_table[value]:
                Exception("Unknwon text-style: %s"%value)
            value = self.style_style_table[value]

        else:
            raise Exception("Unknown style-property %s"%self.__style_prop_name)

        # store value
        self.__style_props[self.__style_prop_name] = value

class BracketsInfo:
    def __init__(self, character, position):
        self.character = character
        self.position  = position

class TextBlockData(QTextBlockUserData):
    def __init__(self, parent = None):
        super(TextBlockData, self).__init__()
        self.braces = []
        self.valid = False

    def insert_brackets_info(self, info):
        self.valid = True
        self.braces.append(info)

    def isValid(self):
        return self.valid

class Highlighter(QSyntaxHighlighter):

    def __init__(self, document,language, styleName='default'):
        super(Highlighter, self).__init__(document)

        self.rules = []
        self.multilines_comment = None

        #Init error format
        self.errors = self.document().parent().errors

        #Brace rule
        self.braces = QRegExp('(\{|\}|\(|\)|\[|\])')

        syntax = XMLSyntaxParser(language)
        self.rules = syntax._grammar
        self.multilines_comment = syntax._comments

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

        print 'errors : %s' % self.errors
        if self.currentBlock().firstLineNumber() in self.errors:
            self.setFormat(0, self.currentBlock().length(), self.styles['error'])

        self.setCurrentBlockState(0)

        # Do multi-line strings
        if self.multilines_comment:
            for index,multilines_comment in enumerate(self.multilines_comment):
                self.match_multiline(text, multilines_comment[0],multilines_comment[1],index+1,multilines_comment[3])

    def match_multiline(self, text, start_delimiter, end_delimiter, in_state, style):
        """Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """

        # If inside triple-single quot:es, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
            #print 'No multiline:',text
        # Otherwise, look for the delimiter on this line
        else:
            start = start_delimiter.indexIn(text)
            # Move past this match
            add = start_delimiter.matchedLength()
            add = 0
            #print 'Multiline:',text

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = end_delimiter.indexIn(text, start + add)
            #print 'end : ', end
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + end_delimiter.matchedLength()
                #print 'Text:',text,', Multiline start : ', start, ', add : ',add, ', end :', end, ', lenght :',length
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
                #print 'Text: ',text,',No Multiline start : ', start, ', add : ',add, ', end :', end, ', lenght :',length
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = start_delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False

if __name__ == '__main__':
    syntax = XMLSyntaxParser('cpp')
    print syntax._grammar
    print syntax._comments
