#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PySide import QtCore, QtGui, QtDeclarative

app = QtGui.QApplication(sys.argv)
model = QtGui.QDirModel()
view = QtDeclarative.QDeclarativeView()
view.rootContext().setContextProperty("dirModel", model)
view.setSource(QtCore.QUrl.fromLocalFile("fileselector.qml"))
view.show()

sys.exit(app.exec_())