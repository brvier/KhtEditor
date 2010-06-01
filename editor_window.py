#!/usr/bin/env python

"""KhtEditor a source code editor by Khertan : Editor Window"""

import sys
import re
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from plugins import init_plugin_system, get_plugins_by_capability
import editor
#import editor_frame
from subprocess import *
import commands
import os

class FindAndReplaceDlg(QtGui.QDialog):

    def __init__(self, parent=None):
        super(FindAndReplaceDlg, self).__init__(parent)

        findLabel = QtGui.QLabel("Find &what:")
        self.findLineEdit = QtGui.QLineEdit()
        findLabel.setBuddy(self.findLineEdit)
        replaceLabel = QtGui.QLabel("Replace w&ith:")
        self.replaceLineEdit = QtGui.QLineEdit()
        replaceLabel.setBuddy(self.replaceLineEdit)
        self.caseCheckBox = QtGui.QCheckBox("&Case sensitive")
        self.wholeCheckBox = QtGui.QCheckBox("Wh&ole words")
        self.wholeCheckBox.setChecked(True)
        moreFrame = QtGui.QFrame()
        moreFrame.setFrameStyle(QtGui.QFrame.StyledPanel|QtGui.QFrame.Sunken)
        self.backwardsCheckBox = QtGui.QCheckBox("Search &Backwards")
        self.regexCheckBox = QtGui.QCheckBox("Regular E&xpression")
        self.ignoreNotesCheckBox = QtGui.QCheckBox("Ignore foot&notes "
                                             "and endnotes")
        line = QtGui.QFrame()
        line.setFrameStyle(QtGui.QFrame.VLine|QtGui.QFrame.Sunken)
        self.findButton = QtGui.QPushButton("&Find")
        self.replaceButton = QtGui.QPushButton("&Replace")
        closeButton = QtGui.QPushButton("Close")
        moreButton = QtGui.QPushButton("&More")
        moreButton.setCheckable(True)
        
        self.findButton.setFocusPolicy(Qt.NoFocus)
        self.replaceButton.setFocusPolicy(Qt.NoFocus)
        closeButton.setFocusPolicy(Qt.NoFocus)
        moreButton.setFocusPolicy(Qt.NoFocus)

        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(findLabel, 0, 0)
        gridLayout.addWidget(self.findLineEdit, 0, 1)
        gridLayout.addWidget(replaceLabel, 1, 0)
        gridLayout.addWidget(self.replaceLineEdit, 1, 1)
        frameLayout = QtGui.QVBoxLayout()
        frameLayout.addWidget(self.backwardsCheckBox)
        frameLayout.addWidget(self.regexCheckBox)
        frameLayout.addWidget(self.ignoreNotesCheckBox)
        moreFrame.setLayout(frameLayout)
        leftLayout = QtGui.QVBoxLayout()
        leftLayout.addLayout(gridLayout)
        leftLayout.addWidget(self.caseCheckBox)
        leftLayout.addWidget(self.wholeCheckBox)
        leftLayout.addWidget(moreFrame)
        buttonLayout = QtGui.QVBoxLayout()
        buttonLayout.addWidget(self.findButton)
        buttonLayout.addWidget(self.replaceButton)
        buttonLayout.addWidget(closeButton)
        buttonLayout.addWidget(moreButton)
        buttonLayout.addStretch()
        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addLayout(leftLayout)
        mainLayout.addWidget(line)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

        moreFrame.hide()
        mainLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
 
        self.connect(moreButton, QtCore.SIGNAL("toggled(bool)"),
                     moreFrame, QtCore.SLOT("setVisible(bool)"))
        self.connect(self.findLineEdit, QtCore.SIGNAL("textEdited(QString)"),
                     self.updateUi)
        self.connect(self.findButton, QtCore.SIGNAL("clicked()"),
                     self.findClicked)
        self.connect(self.replaceButton, QtCore.SIGNAL("clicked()"),
                     self.replaceClicked)

        self.updateUi()
        self.setWindowTitle("Find and Replace")
        

    def findClicked(self):
        self.emit(QtCore.SIGNAL("find"), self.findLineEdit.text(),
                self.caseCheckBox.isChecked(),
                self.wholeCheckBox.isChecked(),
                self.backwardsCheckBox.isChecked(),
                self.regexCheckBox.isChecked(),
                self.ignoreNotesCheckBox.isChecked())
        
        
    def replaceClicked(self):
        self.emit(QtCore.SIGNAL("replace"), self.findLineEdit.text(),
                self.replaceLineEdit.text(),
                self.caseCheckBox.isChecked(),
                self.wholeCheckBox.isChecked(),
                self.backwardsCheckBox.isChecked(),
                self.regexCheckBox.isChecked(),
                self.ignoreNotesCheckBox.isChecked())
        

    def updateUi(self):
        enable = not self.findLineEdit.text().isEmpty()
        self.findButton.setEnabled(enable)
        self.replaceButton.setEnabled(enable)

class Window(QtGui.QMainWindow):
    def __init__(self, parent):
        QtGui.QMainWindow.__init__(self,None)
        self.parent = parent
        
        self.setupFileMenu()
        self.setupHelpMenu()
        self.setupEditor()

        self.setAttribute(QtCore.Qt.WA_Maemo5AutoOrientation, True)
        self.setAttribute(Qt.WA_Maemo5StackedWindow, True)
        self.setCentralWidget(self.editor)
        
        self.findAndReplace = FindAndReplaceDlg()



    def fileSave(self):
        try:
            self.editor.save()
        except (IOError, OSError), e:
            QtGui.QMessageBox.warning(self, "KhtEditor -- Save Error",
                    "Failed to save %s: %s" % (self.fileName, e))

    def saveAsFile(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self,
                        "KhtEditor -- Save File As",
                        self.editor.fileName, "Python files (*.py *.pyw)")
        if not fileName.isEmpty():
            self.editor.fileName = fileName
            self.setWindowTitle(QtCore.QFileInfo(fileName).fileName())
            self.fileSave()

#    def newFile(self):
#        w = Window(self)
#        w.show()

    def openFile(self, path=QtCore.QString()):
        filename = QtGui.QFileDialog.getOpenFileName(self,
                            "KhtEditor -- Open File")
        if not filename.isEmpty():
            self.loadFile(filename)
        return filename


    def loadFile(self, fileName):
        self.editor.fileName = fileName
        try:
            #self.editor.load()
            QtCore.QTimer.singleShot(100, self.editor.load)
            self.setWindowTitle(QtCore.QFileInfo(self.editor.fileName).fileName())
        except (IOError, OSError), e:
            QtGui.QMessageBox.warning(self, "KhtEditor -- Load Error",
                    "Failed to load %s: %s" % (filename, e))

    def setupEditor(self):
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(12)

        self.editor = editor.Kht_Editor(self)
        self.editor.setFont(font)
        #self.editor_frame = editor_frame.Frame(self.editor)
        self.setupToolBar()
        from syntax.python_highlighter import Highlighter
        self.highlighter = Highlighter(self.editor.document())
        self.connect(self.editor.document(),QtCore.SIGNAL('modificationChanged(bool)'),self.do_documentChanged)

    def setupToolBar(self):
        self.toolbar = self.addToolBar('Toolbar')

        commentIcon = QtGui.QIcon.fromTheme("general_tag")
        indentIcon = QtGui.QIcon('icons/tb_indent.png')

        unindentIcon = QtGui.QIcon('icons/tb_unindent.png')
        saveIcon = QtGui.QIcon.fromTheme("notes_save")
        fullscreenIcon = QtGui.QIcon.fromTheme("general_fullsize")
        executeIcon = QtGui.QIcon.fromTheme("general_forward")
        findIcon = QtGui.QIcon.fromTheme("general_search")
  
#        for path in commentIcon.themeSearchPaths():
#            print path

        self.lineCount = QtGui.QLabel('L.1 C.1')                             
        self.toolbar.addWidget(self.lineCount)                                 
        self.connect(self.editor, QtCore.SIGNAL('cursorPositionChanged()'),self.lineCountUpdate)
        self.tb_comment = QtGui.QAction(commentIcon, 'Comment', self)
        #self.tb_comment.setShortcut('Ctrl+S')
        self.connect(self.tb_comment, QtCore.SIGNAL('triggered()'), self.do_comment)
        self.toolbar.addAction(self.tb_comment)
        self.tb_indent = QtGui.QAction(indentIcon, 'Indent', self)
        self.tb_indent.setShortcut('Ctrl+U')
        self.connect(self.tb_indent, QtCore.SIGNAL('triggered()'), self.do_indent)
        self.toolbar.addAction(self.tb_indent)
        self.tb_unindent = QtGui.QAction(unindentIcon, 'Unindent', self)
        self.tb_unindent.setShortcut('Ctrl+I')
        self.connect(self.tb_unindent, QtCore.SIGNAL('triggered()'), self.do_unindent)
        self.toolbar.addAction(self.tb_unindent)
        self.tb_find = QtGui.QAction(findIcon, 'Find', self)
        self.tb_find.setShortcut('Ctrl+F')
        self.connect(self.tb_find, QtCore.SIGNAL('triggered()'), self.do_find)
        self.toolbar.addAction(self.tb_find)
        self.tb_save = QtGui.QAction(saveIcon, 'Save', self)
        self.tb_save.setShortcut('Ctrl+S')
        self.connect(self.tb_save, QtCore.SIGNAL('triggered()'), self.do_save)
        self.toolbar.addAction(self.tb_save)
        self.tb_execute = QtGui.QAction(executeIcon, 'Execute', self)
        self.tb_execute.setShortcut('Ctrl+E')
        self.connect(self.tb_execute, QtCore.SIGNAL('triggered()'), self.do_execute)
        self.toolbar.addAction(self.tb_execute)
        self.tb_fullscreen = QtGui.QAction(fullscreenIcon, 'Execute', self)          
        self.connect(self.tb_fullscreen, QtCore.SIGNAL('triggered()'), self.do_fullscreen)
        self.toolbar.addAction(self.tb_fullscreen)
  
    def setupFileMenu(self): 
        fileMenu = QtGui.QMenu(self.tr("&File"), self)
        self.menuBar().addMenu(fileMenu)

        fileMenu.addAction(self.tr("New..."), self.parent.newFile,
                QtGui.QKeySequence(self.tr("Ctrl+N", "New")))
        fileMenu.addAction(self.tr("Open..."), self.parent.openFile,
                QtGui.QKeySequence(self.tr("Ctrl+O", "Open")))
        fileMenu.addAction(self.tr("Save As"), self.saveAsFile,
                QtGui.QKeySequence(self.tr("Ctrl+Maj+S", "Save As")))

    def setupHelpMenu(self):
        helpMenu = QtGui.QMenu(self.tr("&Help"), self)
        self.menuBar().addMenu(helpMenu)

        helpMenu.addAction(self.tr("&About"), self.do_about)
        
    def do_about(self):
        self.parent.about(self)
        
    def do_indent(self):
        self.editor.indent()

    def do_unindent(self):
        self.editor.unIndent()
        
    def do_comment(self):
        self.editor.comment()
        
    def do_save(self):
        self.fileSave()
        
    def do_find(self):
        self.findAndReplace.connect(self.findAndReplace, QtCore.SIGNAL("find"), self.editor.find)
        self.findAndReplace.show()
        
    def do_execute(self):
        print "execute"
        #ask for save if unsaved
        self.fileSave()
    
        if self.editor.fileName != None:
#          note = osso.SystemNote(self._parent.context)
#          result = note.system_note_infoprint("Launching "+ self.filepath +" ...")
    
          fileHandle = open('/tmp/khteditor.tmp', 'w')
          fileHandle.write('#!/bin/sh\n')
          fileHandle.write('cd '+os.path.dirname(str(self.editor.fileName))+' \n')
          fileHandle.write("python \'"+self.editor.fileName + "\'\n")
          fileHandle.write('read -p "Press ENTER to continue ..." foo')
          fileHandle.write('\nexit')
          fileHandle.close()
          commands.getoutput("chmod 777 /tmp/khteditor.tmp")
          Popen('/usr/bin/osso-xterm /tmp/khteditor.tmp',shell=True,stdout=None)
    
    def lineCountUpdate(self):
        cursor = self.editor.textCursor()
        self.lineCount.setText("L.%d C.%d" % (cursor.blockNumber()+1,cursor.columnNumber()+1))
        
    def closeEvent(self,widget,*args):
#        print 'call editor close event'
        self.editor.closeEvent()
       
    def do_fullscreen(self):
        if self.isFullScreen():
            self.showMaximized()
        else:
            self.showFullScreen() 

    def do_documentChanged(self,changed):
        if changed == True:
            self.setWindowTitle('*'+QtCore.QFileInfo(self.editor.fileName).fileName())
        else:
            self.setWindowTitle(QtCore.QFileInfo(self.editor.fileName).fileName())

