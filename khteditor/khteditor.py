#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Benoît HERVIER
# Licenced under GPLv3

from PySide.QtGui import QApplication, QFileDialog
from PySide.QtCore import Slot, QSettings

import os.path
import sys
from plugins.plugins_api import init_plugin_system, \
                                find_plugins
from window import KhtWindow

__version__ = '2.0.0'


class KhtEditor(QApplication):
    def __init__(self):
        QApplication.__init__(self,sys.argv)
        self.setOrganizationName("Khertan Software")
        self.setOrganizationDomain("khertan.net")
        self.setApplicationName("KhtEditor")

        self.windows = []

        #Initialization of the plugin system
        init_plugin_system()

        #Got the enabled plugin
        settings =  QSettings()
        self.enabled_plugins = []
        for plugin in find_plugins():
            if settings.contains(plugin.__name__):
                if settings.value(plugin.__name__) == '2':
                    print 'Enable plugin ', plugin
                    self.enabled_plugins.append(plugin())

        #Open file passed as args
        for arg in sys.argv[1:]:
            if os.path.exists(arg):
                print 'path:',arg
                self.openFile(filepath = arg)
        if len(self.windows) == 0:
            self.newWindow()

    def newWindow(self):
        win = KhtWindow(enabled_plugins=self.enabled_plugins)
        win.closed.connect(self.closedWindow)
        win.setWindowTitle('New File')
        win.tb_openFile.connect(self.openFile)
        self.windows.append(win)
        return win

    def openFile(self, path = None, filepath = None):
        if not path:
            path = '/home/user/MyDocs'
        if not filepath:
            filepath, ok =  QFileDialog.getOpenFileName(self.sender(),
                            "KhtEditor -- Open File",path)
        if filepath:
            win = self.newWindow()          
            win.editor.setFilePath(filepath)
            win.editor.load()

    @Slot()
    def closedWindow(self):
        try:
            self.windows.remove(self.sender())
        except KeyError, err:
            print err

if __name__ == '__main__':
    sys.exit(KhtEditor().exec_())
