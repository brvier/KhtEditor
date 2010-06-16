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
    """ Find and replace dialog """
    def __init__(self, parent=None):
        super(FindAndReplaceDlg, self).__init__(parent)

        findLabel = QtGui.QLabel("Find &what:")
        self.findLineEdit = QtGui.QLineEdit()
        #Remove auto capitalization
        self.findLineEdit.setInputMethodHints(Qt.ImhNoAutoUppercase)
        findLabel.setBuddy(self.findLineEdit)
        replaceLabel = QtGui.QLabel("Replace w&ith:")
        self.replaceLineEdit = QtGui.QLineEdit()
        #Remove auto capitalization
        self.replaceLineEdit.setInputMethodHints(Qt.ImhNoAutoUppercase)
        replaceLabel.setBuddy(self.replaceLineEdit)
        self.caseCheckBox = QtGui.QCheckBox("&Case sensitive")
        self.wholeCheckBox = QtGui.QCheckBox("Wh&ole words")
        moreFrame = QtGui.QFrame()
        moreFrame.setFrameStyle(QtGui.QFrame.StyledPanel|QtGui.QFrame.Sunken)
        self.backwardsCheckBox = QtGui.QCheckBox("Search &Backwards")
        self.regexCheckBox = QtGui.QCheckBox("Regular E&xpression")
        line = QtGui.QFrame()
        line.setFrameStyle(QtGui.QFrame.VLine|QtGui.QFrame.Sunken)
        self.findButton = QtGui.QPushButton("&Find")
        self.replaceButton = QtGui.QPushButton("&Replace")
        self.replaceAllButton = QtGui.QPushButton("&ReplaceAll")
        
        self.findButton.setFocusPolicy(Qt.NoFocus)
        self.replaceButton.setFocusPolicy(Qt.NoFocus)
        self.replaceAllButton.setFocusPolicy(Qt.NoFocus)

        gridLayout = QtGui.QGridLayout()
        leftLayout = QtGui.QVBoxLayout()
        gridLayout.addWidget(findLabel, 0, 0)
        gridLayout.addWidget(self.findLineEdit, 0, 1)
        gridLayout.addWidget(replaceLabel, 1, 0)
        gridLayout.addWidget(self.replaceLineEdit, 1, 1)
        gridLayout.addWidget(self.caseCheckBox, 2, 0)
        gridLayout.addWidget(self.wholeCheckBox, 2, 1)
        gridLayout.addWidget(self.backwardsCheckBox, 3, 0)
        gridLayout.addWidget(self.regexCheckBox, 3,1)
        leftLayout.addLayout(gridLayout)
        buttonLayout = QtGui.QVBoxLayout()
        buttonLayout.addWidget(self.findButton)
        buttonLayout.addWidget(self.replaceButton)
        buttonLayout.addWidget(self.replaceAllButton)
        buttonLayout.addStretch()
        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addLayout(leftLayout)
        mainLayout.addWidget(line)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

        mainLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
 
        self.connect(self.findLineEdit, QtCore.SIGNAL("textEdited(QString)"),
                     self.updateUi)
        self.connect(self.findButton, QtCore.SIGNAL("clicked()"),
                     self.findClicked)
        self.connect(self.replaceButton, QtCore.SIGNAL("clicked()"),
                     self.replaceClicked)
        self.connect(self.replaceAllButton, QtCore.SIGNAL("clicked()"),
                     self.replaceAllClicked)
        self.updateUi()
        self.setWindowTitle("Find and Replace")
        

    def findClicked(self):
        self.emit(QtCore.SIGNAL("find"), self.findLineEdit.text(),
                self.caseCheckBox.isChecked(),
                self.wholeCheckBox.isChecked(),
                self.backwardsCheckBox.isChecked(),
                self.regexCheckBox.isChecked(),)
        self.hide()
        
        
    def replaceClicked(self):
        self.emit(QtCore.SIGNAL("replace"), self.findLineEdit.text(),
                self.replaceLineEdit.text(),
                self.caseCheckBox.isChecked(),
                self.wholeCheckBox.isChecked(),
                self.backwardsCheckBox.isChecked(),
                self.regexCheckBox.isChecked(),)
        self.hide()
        
    def replaceAllClicked(self):
        self.emit(QtCore.SIGNAL("replaceAll"), self.findLineEdit.text(),
                self.replaceLineEdit.text(),
                self.caseCheckBox.isChecked(),
                self.wholeCheckBox.isChecked(),
                self.backwardsCheckBox.isChecked(),
                self.regexCheckBox.isChecked(),)
        self.hide()        

    def updateUi(self):
        enable = not self.findLineEdit.text().isEmpty()
        self.findButton.setEnabled(enable)
        self.replaceButton.setEnabled(enable)
        self.replaceAllButton.setEnabled(enable)        

class Window(QtGui.QMainWindow):
    def __init__(self, parent):
        QtGui.QMainWindow.__init__(self,None)
        self.parent = parent
        
        self.findAndReplace = FindAndReplaceDlg()               
        self.setupFileMenu()
        self.setupHelpMenu()
        self.setupEditor()

        self.setAttribute(QtCore.Qt.WA_Maemo5AutoOrientation, True)
        self.setAttribute(Qt.WA_Maemo5StackedWindow, True)
        
#        self.area = QtGui.QScrollArea(self)
#        self.area.setWidget(self.editor)
#        self.area.setWidgetResizable(True)

#        scroller = self.area.property("kineticScroller").toPyObject()
#        scroller.setEnabled(True)

        self.setCentralWidget(self.editor)

        #Initialization of the plugin system
        init_plugin_system({'plugin_path': '/home/opt/khteditor/plugins',
                            'plugins': ['autoindent','pylint']})
        
        
    def fileSave(self):
        try:
            self.editor.save()
        except (IOError, OSError), e:
            QtGui.QMessageBox.warning(self, "KhtEditor -- Save Error",
                    "Failed to save %s: %s" % (self.filename, e))


    def saveAsFile(self):
        filename = QtGui.QFileDialog.getSaveFileName(self,
                        "KhtEditor -- Save File As",
                        self.editor.filename, "Python files (*.py *.pyw)")
        if not filename.isEmpty():
            self.editor.filename = filename
            self.setWindowTitle(QtCore.QFileInfo(filename).fileName())
            self.fileSave()


    def openFile(self, path=QtCore.QString()):
        filename = QtGui.QFileDialog.getOpenFileName(self,
                            "KhtEditor -- Open File",path)
        if not filename.isEmpty():
            self.loadFile(filename)
        return filename


    def loadFile(self, filename):
        self.editor.filename = filename
        try:
            self.editor.load()
#            QtCore.QTimer.singleShot(100, self.editor.load)
            self.setWindowTitle(QtCore.QFileInfo(self.editor.filename).fileName())
        except (IOError, OSError), e:
            QtGui.QMessageBox.warning(self, "KhtEditor -- Load Error",
                    "Failed to load %s: %s" % (filename, e))

    def setupEditor(self):
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(12)

        self.editor = editor.KhtTextEdit(self)
        self.editor.setFont(font)
        #self.editor_frame = editor_frame.Frame(self.editor)
        self.setupToolBar()
        from syntax.python_highlighter import Highlighter
        self.highlighter = Highlighter(self.editor.document())
        self.connect(self.editor.document(),
            QtCore.SIGNAL('modificationChanged(bool)'),self.do_documentChanged)

    def setupToolBar(self):
        self.toolbar = self.addToolBar('Toolbar')

        commentIcon = QtGui.QIcon.fromTheme("general_tag")
        indentIcon = QtGui.QIcon('/home/opt/khteditor/icons/tb_indent.png')

        unindentIcon = QtGui.QIcon('/home/opt/khteditor/icons/tb_unindent.png')
        saveIcon = QtGui.QIcon.fromTheme("notes_save")
        fullscreenIcon = QtGui.QIcon.fromTheme("general_fullsize")
        executeIcon = QtGui.QIcon.fromTheme("general_forward")
        findIcon = QtGui.QIcon.fromTheme("general_search")

        self.lineCount = QtGui.QLabel('L.1 C.1')                             
        self.toolbar.addWidget(self.lineCount)                                 
        self.connect(self.editor, 
                QtCore.SIGNAL('cursorPositionChanged()'),self.lineCountUpdate)
        self.tb_comment = QtGui.QAction(commentIcon, 'Comment', self)
        self.connect(self.tb_comment, QtCore.SIGNAL('triggered()'), self.editor.comment)
        self.toolbar.addAction(self.tb_comment)
        self.tb_indent = QtGui.QAction(indentIcon, 'Indent', self)
        self.tb_indent.setShortcut('Ctrl+I')
        self.connect(self.tb_indent, QtCore.SIGNAL('triggered()'), self.editor.indent)
        self.toolbar.addAction(self.tb_indent)
        self.tb_unindent = QtGui.QAction(unindentIcon, 'Unindent', self)
        self.tb_unindent.setShortcut('Ctrl+U')
        self.connect(self.tb_unindent, QtCore.SIGNAL('triggered()'), self.editor.unindent)
        self.toolbar.addAction(self.tb_unindent)
        self.tb_find = QtGui.QAction(findIcon, 'Find', self)
        self.tb_find.setShortcut('Ctrl+F')
        self.connect(self.tb_find, QtCore.SIGNAL('triggered()'), self.do_find)
        self.toolbar.addAction(self.tb_find)
        self.tb_save = QtGui.QAction(saveIcon, 'Save', self)
        self.tb_save.setShortcut('Ctrl+S')
        self.connect(self.tb_save, QtCore.SIGNAL('triggered()'), self.fileSave)
        self.toolbar.addAction(self.tb_save)
        self.tb_execute = QtGui.QAction(executeIcon, 'Execute', self)
        self.tb_execute.setShortcut('Ctrl+E')
        self.connect(self.tb_execute, QtCore.SIGNAL('triggered()'), self.do_execute)
        self.toolbar.addAction(self.tb_execute)
        self.tb_fullscreen = QtGui.QAction(fullscreenIcon, 'Execute', self)          
        self.connect(self.tb_fullscreen, QtCore.SIGNAL('triggered()'), self.do_fullscreen)
        self.toolbar.addAction(self.tb_fullscreen)

        #Actions not in toolbar
        self.tb_duplicate = QtGui.QAction('Duplicate', self)          
        self.tb_duplicate.setShortcut('Ctrl+D')
        self.connect(self.tb_duplicate,
             QtCore.SIGNAL('triggered()'), self.editor.duplicate)
        self.addAction(self.tb_duplicate)
        self.tb_findagain = QtGui.QAction('Find Again', self)          
        self.tb_findagain.setShortcut('Ctrl+G')
        self.connect(self.tb_findagain,
             QtCore.SIGNAL('triggered()'), self.findAndReplace.findClicked)
        self.addAction(self.tb_findagain)

        
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
        
#    def do_indent(self):
#        self.editor.indent()

#    def do_unindent(self):
#        self.editor.unindent()
        
#    def do_comment(self):
#        self.editor.comment()
        
#    def do_save(self):
#        self.fileSave()
        
#    def do_duplicate(self):
#        self.editor.duplicate()
        
#    def do_findagain(self):
#        self.findAndReplace.findClicked()
        
    def do_find(self):
        self.findAndReplace.connect(self.findAndReplace,
                         QtCore.SIGNAL("find"), self.editor.find)
        self.findAndReplace.connect(self.findAndReplace,
                         QtCore.SIGNAL("replace"), self.editor.replace)
        self.findAndReplace.connect(self.findAndReplace,
                         QtCore.SIGNAL("replaceAll"), self.editor.replace_all)
        self.findAndReplace.show()
        
    def do_execute(self):
        print "execute"
        #ask for save if unsaved
        self.fileSave()
    
        if self.editor.filename != None:
          fileHandle = open('/tmp/khteditor.tmp', 'w')
          fileHandle.write('#!/bin/sh\n')
          fileHandle.write('cd '+os.path.dirname(str(self.editor.filename))+' \n')
          fileHandle.write("python \'"+self.editor.filename + "\'\n")
          fileHandle.write('read -p "Press ENTER to continue ..." foo')
          fileHandle.write('\nexit')
          fileHandle.close()
          commands.getoutput("chmod 777 /tmp/khteditor.tmp")
          Popen('/usr/bin/osso-xterm /tmp/khteditor.tmp',shell=True,stdout=None)
    
    def lineCountUpdate(self):
        cursor = self.editor.textCursor()
        self.lineCount.setText("L.%d C.%d" % (cursor.blockNumber()+1, 
                                            cursor.columnNumber()+1))
        
    def closeEvent(self,widget,*args):
        self.editor.closeEvent()
       
    def do_fullscreen(self):
        if self.isFullScreen():
            self.showMaximized()
        else:
            self.showFullScreen() 

    def do_documentChanged(self,changed):
        if changed == True:
            self.setWindowTitle('*'+QtCore.QFileInfo(self.editor.filename).fileName())
        else:
            self.setWindowTitle(QtCore.QFileInfo(self.editor.filename).fileName())

