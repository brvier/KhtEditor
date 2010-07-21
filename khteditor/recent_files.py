#!/usr/bin/env python

"""KhtEditor a source code editor by Khertan : Recent Files Managment"""

from PyQt4.QtCore import QSettings,QVariant

class RecentFiles():
    def __init__(self):
       self.settings = QSettings()
       
    def get(self):
       return self.settings.value("RecentFiles").toStringList()
       
    def append(self,path):
        recentFiles = self.get()
        #Insert if didn't exist yet else put in top
        pos = recentFiles.indexOf(path)
        if pos > -1:
            recentFiles.takeAt(pos)
        recentFiles.prepend(path)
        #Limit to ten recent files
        recentFiles = recentFiles[:10]
        #Save them
        recentFilesVariant = QVariant(recentFiles) \
              if recentFiles else QVariant()
        self.settings.setValue('RecentFiles',recentFilesVariant)