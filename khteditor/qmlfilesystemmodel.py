#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Benoît HERVIER
# Licenced under GPLv3

from PySide.QtGui import QApplication, QFileSystemModel
from PySide.QtCore import QObject, QUrl, QDir, Slot, QModelIndex
from PySide import QtDeclarative

class QmlFileSystemModel(QFileSystemModel):
    def __init__(self, parent=None):
        QFileSystemModel.__init__(self, parent)
    
    @Slot(QModelIndex, result=bool)
    def isDir(self, index):
        return QFileSystemModel.isDir(self,index)

    @Slot(QModelIndex, result=unicode)
    def filePath(self, index):
        return QFileSystemModel.filePath(self,index)
