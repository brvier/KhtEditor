#!/usr/bin/env python

"""KhtEditor a source code editor by Khertan : Code Editor"""

import sys
import re
from PyQt4 import QtCore, QtGui
from plugins import init_plugin_system, get_plugins_by_capability

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
