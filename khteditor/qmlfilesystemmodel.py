#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Benoît HERVIER
# Licenced under GPLv3

from PySide.QtGui import QApplication, QFileSystemModel
from PySide.QtCore import QObject, QUrl, QDir, Slot, QModelIndex
from PySide import QtDeclarative

import os.path

class QmlFileSystemModel(QFileSystemModel):
    def __init__(self, parent=None):
        QFileSystemModel.__init__(self, parent)
        self.currentIndex = QFileSystemModel.index(self,os.path.expanduser('~/'))

    @Slot(result=QModelIndex)
    def getCurrentIndex(self):
        return self.currentIndex

    @Slot(unicode)
    def setCurrentPath(self, path):
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        self.currentIndex = QFileSystemModel.index(self,path)
    
    @Slot(QModelIndex, result=bool)
    def isDir(self, index):
        return QFileSystemModel.isDir(self,index)

    @Slot(QModelIndex, result=unicode)
    def filePath(self, index):
        return QFileSystemModel.filePath(self,index)

#    @Slot(unicode, result=QModelIndex)
#    def index(self, path):
#        return QFileSystemModel.index(self,path)
