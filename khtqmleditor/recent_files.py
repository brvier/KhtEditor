#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Benoît HERVIER
# Licenced under GPLv3

"""KhtEditor a source code editor by Khertan : Recent Files Managment"""

from PySide.QtCore import QSettings

class RecentFiles():
    def __init__(self):
       self.settings = QSettings()

    def get(self):
       return self.settings.value("RecentFiles")

    def append(self,path):
        recentFiles = self.get()

        #Insert if didn't exist yet else put in top
        if recentFiles == None:
            recentFiles = []

        #Bug 60
        if type(recentFiles) in (str,unicode):
            recentFiles = [recentFiles,]

        if path in recentFiles:
            recentFiles.pop(recentFiles.index(path))
        recentFiles.insert(0, path)

        #Limit to ten recent files
        recentFiles = recentFiles[:10]

        #Save them
        self.settings.setValue('RecentFiles',recentFiles)
