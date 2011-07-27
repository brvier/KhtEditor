#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Benoît HERVIER
# Licenced under GPLv3

from PySide.QtDeclarative import QDeclarativeItem
from PySide.QtGui import QGraphicsProxyWidget, QGraphicsItem
from PySide.QtCore import QSize, Slot, Property, Signal, QRect

class QmlExecutor(QDeclarativeItem):
    textChanged = Signal()

    def __init__(self, parent=None):
        QDeclarativeItem.__init__(self, parent)

        self.widget = QPlainTextEdit
        self.widget.resize(850,480)
        self.widget.setReadOnly(True)
        self.proxy = QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.widget)
        self.proxy.setPos(0,0)
        self.setFlag(QGraphicsItem.ItemHasNoContents, False)
        self.widget.sizeChanged.connect(self.sizeChanged)
        self._width = self.widget.width()
        self._height = self.widget.height()
        #self.widget.filepathChanged.connect(self.filepathChanged)
        self._modification = False
        self.widget.modificationChanged.connect(self.setModificationChanged)
        self.widget.positionTextChanged.connect(self.setPositionText)
        self.widget.cursorRectangleChanged.connect(self.setCursorRectangle)


    @Slot(unicode)
    def run(self, command):
        self._command = command

        self._processLog = QProcess()
        self._processLog.readyReadStandardOutput.connect(self._readLog)        
        self._processLog.start(self._command)

    @Slot()
    def _readLog(self):
        while self._processLog.canReadLine():
            self.widget.appendPlainText(unicode(self._processLog.readLine()))
