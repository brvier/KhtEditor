#!/usr/bin/env python

"""KhtEditor a source code editor by Khertan : Welcome Window"""

import sys
from PyQt4 import QtCore, QtGui
import editor_window

class WelcomeWindow(QtGui.QMainWindow):
    def __init__(self, parent=None, main=None):
        super(WelcomeWindow, self).__init__(parent)
        self.resize(800, 480)

        self.setupMenu()
        self.setupMain()

        self.main = main
        self.main.window_list.append(self)

#        self.setCentralWidget(self.layout)
#        self.setLayout(self.layout)
        self.setWindowTitle(self.tr("KhtEditor"))

    def about(self):
        QtGui.QMessageBox.about(self, self.tr("About KhtEditor"),
                self.tr("<p><b>KhtEditor</b> is a source code editor "
                        "Mainly designed for Maemo and Meego.</p>"))

    def newFile(self):
        w = editor_window.Window(None,self.main)
        w.show()

    def openFile(self, path=QtCore.QString()):
        fileName = QtCore.QString(path)

        if fileName.isNull():
            fileName = QtGui.QFileDialog.getOpenFileName(self,
                    self.tr("Open File"), "", "C++ Files (*.cpp *.h *.py)")

        if not fileName.isEmpty():
            editor_win=editor_window.Window(None,self.main)
            editor_win.show()
            editor_win.openFile(fileName)

#            inFile = QtCore.QFile(fileName)
#            if inFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
#                self.editor.setPlainText(QtCore.QString(inFile.readAll()))

    def setupMain(self):
        self.layout = QtGui.QVBoxLayout()


    def setupMenu(self):
        fileMenu = QtGui.QMenu(self.tr("&Menu"), self)
        self.menuBar().addMenu(fileMenu)

        fileMenu.addAction(self.tr("&New..."), self.newFile,
                QtGui.QKeySequence(self.tr("Ctrl+N", "New")))
        fileMenu.addAction(self.tr("&Open..."), self.openFile,
                QtGui.QKeySequence(self.tr("Ctrl+O", "Open")))
        fileMenu.addAction(self.tr("&About"), self.about)
        fileMenu.addAction(self.tr("About &Qt"), QtGui.qApp.aboutQt)