#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Benoît HERVIER
# Licenced under GPLv3

"""PyFlakes Plugin : A KhtEditor plugin to check simple syntax error
   Using PyFlakes """

from PySide.QtCore import Qt, QObject

from PySide.QtGui import QTextEdit, QTextCursor

import sys
try:
    from plugins_api import Plugin
except:
    from khteditor.plugins.plugins_api import Plugin

import compiler
from pyflakes.checker import Checker


class PyFlakes_plugin(Plugin, QObject):
    """ PyFlakes Plugin """

    capabilities = ['afterFileSave','afterFileOpen','beforeCursorPositionChanged']
    __version__ = '0.5'
    thread = None
    def __init__(self):
        QObject.__init__(self)

    def do_afterFileOpen(self, parent):
        self.do_check(parent)

    def do_afterFileSave(self, parent):
        self.do_check(parent)

    def do_beforeCursorPositionChanged(self, parent):
        try:
            doc = parent.document()
            if hasattr(doc,'errors'):
                if len(doc.errors):
                    cur = parent.textCursor()
                    linepos = cur.blockNumber()
                    if linepos in doc.errors:
                        parent.showError.emit(doc.errors[linepos])
        except:
            pass #No Dbus

    def do_check(self, parent):
        """ Do the pylint check and appends in the highlighter errors"""

        #Limit to python source file

        doc = parent.document()
        doc.errors = {}

        if (not parent.getFilePath().endswith('.py')) and (not parent.getFilePath().endswith('.pyw')):
            return

        errors = []
        rows = parent.errors.keys()
        for row in rows:
            parent.highlighter.rehighlightBlock(doc.findBlockByLineNumber(row))

        try:
            ast = compiler.parse(parent.toPlainText().encode('ascii', 'ignore'))
            c = Checker(ast, parent.getFilePath())
            c.messages.sort(lambda a, b: cmp(a.lineno, b.lineno))
            for msg in c.messages:
                try:
                    args = msg.message_args
                    errors.append(((msg.lineno-1, 0, len(args[0])), msg.message % args, False))
                except Exception,err:
                    print err

        except SyntaxError, e:
            row, col = (e.lineno-1, e.offset-1)
            length = len(e.text)
            msg = e.msg
            errors.extend([((row, col, length), msg, True)])
        except Exception, err:
            import traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print 'Flakes plugin : %s' % repr(traceback.format_exception(exc_type, exc_value, \
                                      exc_traceback))

#        selections = []
        for ((row, col, length), msg, is_fatal) in errors:
            doc.errors[row] = msg
            parent.highlighter.rehighlightBlock(doc.findBlockByLineNumber(row))
        parent.documentErrorsChanged.emit()
