#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Benoît HERVIER
# Licenced under GPLv3

from PySide.QtDeclarative import QDeclarativeItem
from PySide.QtGui import QGraphicsProxyWidget, QGraphicsItem
from PySide.QtCore import QSize, Slot, Property, Signal, QRect
from editor import KhtTextEditor

class QmlTextEditor(QDeclarativeItem):
    heightChanged = Signal()
    widthChanged = Signal()
    filepathChanged = Signal()
    modificationChanged = Signal()
    positionTextChanged = Signal()
    cursorRectangleChanged = Signal()

    def __init__(self, parent=None):
        QDeclarativeItem.__init__(self, parent)

        self.widget = KhtTextEditor(inQML=True)
        self.widget.resize(850,480)
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
        self._positionText = '001-001'
        self._cursorRectangle = QRect (1,1,1,1)

    @Slot()
    def indent(self):
        self.widget.indent()

    @Slot()
    def unindent(self):
        self.widget.unindent()

    @Slot(unicode)
    def loadFile(self, filepath):
        self.widget.setFilePath(filepath)
        self.widget.load()

    @Slot()
    def comment(self):
        self.widget.comment()

    @Slot()
    def saveFile(self):
        self.widget.save()

    @Slot()
    def execute(self):
        self.widget.execute()

    @Slot()
    def duplicate(self):
        self.widget.duplicate()

    @Slot(QSize)
    def sizeChanged(self,size):
        self.setWidth(size.width())
        self.setHeight(size.height())

    def getModificationChanged(self): return self._modification
    def setModificationChanged(self, changed):
        if changed != self._modification:
            print 'Changed:',self._modification
            self._modification = changed
            self.modificationChanged.emit()

#    def getFilepath(self): return self.widget.getFilePath()
    @Slot(unicode)
    def setFilepath(self,filepath):
        if filepath:
            if self.widget.getFilePath() != filepath:
                self.widget.setFilePath(filepath)

#                self.widget.load()
                #self.filepathChanged.emit()

    def getWidth(self): return self._width
    def setWidth(self,width):
        if width != self._width:
            self._width = width
            self.widthChanged.emit()

    def getHeight(self): return self._height
    def setHeight(self,height):
        if height != self._height:
            self._height = height
            self.heightChanged.emit()

    def setCursorRectangle(self,rect):
        if self._cursorRectangle != rect:
            self._cursorRectangle =rect
            self.cursorRectangleChanged.emit()
    def getCursorRectangle(self): return self._cursorRectangle

    def getPositionText(self): return self._positionText
    def setPositionText(self, text):
        if self._positionText != text:
            self._positionText = text
            self.positionTextChanged.emit()

    width = Property(int,getWidth, setWidth, notify=widthChanged)
    height = Property(int, getHeight, setHeight, notify=heightChanged)
#    filepath = Property(unicode, getFilepath, setFilepath)
    modification = Property(bool, getModificationChanged, setModificationChanged, notify=modificationChanged)
    positionText = Property(unicode, getPositionText, setPositionText, notify=positionTextChanged)
    cursorRectangle = Property(QRect, getCursorRectangle, setCursorRectangle, notify=cursorRectangleChanged)

