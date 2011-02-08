#!/usr/bin/env python

"""KhtEditor a source code editor by Khertan : Editor Window"""

import sys
import re

from PyQt4.QtGui import QMainWindow, \
    QHBoxLayout, \
    QVBoxLayout, \
    QFileDialog, \
    QScrollArea, \
    QCheckBox, \
    QDialog, \
    QGridLayout, \
    QLineEdit, \
    QFrame, \
    QLabel, \
    QPushButton, \
    QFont, \
    QKeySequence, \
    QLayout, \
    QMenu, \
    QAction, \
    QApplication, \
    QIcon, \
    QMessageBox

from PyQt4.QtCore import QFileInfo, \
    Qt, \
    QTimer, \
    QSettings, \
    pyqtSlot,pyqtSignal
    
from PyQt4.QtCore import Qt

from plugins.plugins_api import init_plugin_system, filter_plugins_by_capability, find_plugins, Plugin
import editor
#import editor_frame
from subprocess import *
import commands
import os

LANGUAGES = (('.R','R'),
            ('.ada','ada'),
            ('.c','c'),
            ('.changelog','changelog'),
            ('.cpp','cpp'),
            ('.csharp','csharp'),
            ('.desktop','desktop'),
            ('.css','css'),
            ('.diff','diff'),
            ('.fort','fortran'),
            ('.gtkrc','gtkrc'),
            ('.haskell','haskell'),
            ('.html','html'),
            ('.idl','idl'),
            ('.ini','ini'),
            ('.java','java'),
            ('.js','javascript'),
            ('.tex','latex'),
            ('.lua','lua'),
            ('makefile','makefile'),
            ('markdown','markdown'),
            ('.msil','msil'),
            ('nemerle','nemerle'),
            ('octave','octave'),
            ('.pas','pascal'),
            ('.pl','perl'),
            ('.php','php'),
            ('.po','po'),
            ('.py','python'),
            ('.qml','qml'),
            ('.rb','ruby'),
            ('.scheme','scheme'),
            ('.sh','sh'),
            ('.tcl','tcl'),
            ('texinfo','texinfo'),
            ('.txt','None'),
            ('.vb','vbnet'),
            ('verilog','verilog'),
            ('vhdl','vhdl'),
            ('.xml','xml'),
            )
class FindAndReplaceDlg( QDialog):
    """ Find and replace dialog """
    find = pyqtSignal(unicode,bool,bool,bool,bool)
    replace = pyqtSignal(unicode,bool,bool,bool,bool)
    replaceAll = pyqtSignal(unicode,bool,bool,bool,bool)
    
    def __init__(self, parent=None):
        super(FindAndReplaceDlg, self).__init__(parent)

        findLabel =  QLabel("Find &what:")
        self.findLineEdit =  QLineEdit()
        #Remove auto capitalization
        self.findLineEdit.setInputMethodHints(Qt.ImhNoAutoUppercase)
        findLabel.setBuddy(self.findLineEdit)
        replaceLabel =  QLabel("Replace w&ith:")
        self.replaceLineEdit =  QLineEdit()
        #Remove auto capitalization
        self.replaceLineEdit.setInputMethodHints(Qt.ImhNoAutoUppercase)
        replaceLabel.setBuddy(self.replaceLineEdit)
        self.caseCheckBox =  QCheckBox("&Case sensitive")
        self.wholeCheckBox =  QCheckBox("Wh&ole words")
        moreFrame =  QFrame()
        moreFrame.setFrameStyle( QFrame.StyledPanel| QFrame.Sunken)
        self.backwardsCheckBox =  QCheckBox("Search &Backwards")
        self.regexCheckBox =  QCheckBox("Regular E&xpression")
        line =  QFrame()
        line.setFrameStyle( QFrame.VLine| QFrame.Sunken)
        self.findButton =  QPushButton("&Find")
        self.replaceButton =  QPushButton("&Replace")
        self.replaceAllButton =  QPushButton("&ReplaceAll")

        self.findButton.setFocusPolicy(Qt.NoFocus)
        self.replaceButton.setFocusPolicy(Qt.NoFocus)
        self.replaceAllButton.setFocusPolicy(Qt.NoFocus)

        gridLayout =  QGridLayout()
        leftLayout =  QVBoxLayout()
        gridLayout.addWidget(findLabel, 0, 0)
        gridLayout.addWidget(self.findLineEdit, 0, 1)
        gridLayout.addWidget(replaceLabel, 1, 0)
        gridLayout.addWidget(self.replaceLineEdit, 1, 1)
        gridLayout.addWidget(self.caseCheckBox, 2, 0)
        gridLayout.addWidget(self.wholeCheckBox, 2, 1)
        gridLayout.addWidget(self.backwardsCheckBox, 3, 0)
        gridLayout.addWidget(self.regexCheckBox, 3,1)
        leftLayout.addLayout(gridLayout)
        buttonLayout =  QVBoxLayout()
        buttonLayout.addWidget(self.findButton)
        buttonLayout.addWidget(self.replaceButton)
        buttonLayout.addWidget(self.replaceAllButton)
        buttonLayout.addStretch()
        mainLayout =  QHBoxLayout()
        mainLayout.addLayout(leftLayout)
        mainLayout.addWidget(line)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

        mainLayout.setSizeConstraint( QLayout.SetFixedSize)

        self.findLineEdit.textEdited.connect(self.updateUi)
        self.findButton.clicked.connect(self.findClicked)
        self.replaceButton.clicked.connect(self.replaceClicked)
        self.replaceAllButton.clicked.connect(self.replaceAllClicked)
        self.updateUi()
        self.setWindowTitle("Find and Replace")


    def findClicked(self):
        self.find.emit( unicode(self.findLineEdit.text()),
                self.caseCheckBox.isChecked(),
                self.wholeCheckBox.isChecked(),
                self.backwardsCheckBox.isChecked(),
                self.regexCheckBox.isChecked(),)
        self.hide()


    def replaceClicked(self):
        self.replace.emit( self.findLineEdit.text(),
                self.replaceLineEdit.text(),
                self.caseCheckBox.isChecked(),
                self.wholeCheckBox.isChecked(),
                self.backwardsCheckBox.isChecked(),
                self.regexCheckBox.isChecked(),)
        self.hide()

    def replaceAllClicked(self):
        self.replaceAll.emit( self.findLineEdit.text(),
                self.replaceLineEdit.text(),
                self.caseCheckBox.isChecked(),
                self.wholeCheckBox.isChecked(),
                self.backwardsCheckBox.isChecked(),
                self.regexCheckBox.isChecked(),)
        self.hide()

    def updateUi(self):
        enable = not (self.findLineEdit.text() == '')
        self.findButton.setEnabled(enable)
        self.replaceButton.setEnabled(enable)
        self.replaceAllButton.setEnabled(enable)

class Window( QMainWindow):    
    def __init__(self, parent):
        global isMAEMO
        QMainWindow.__init__(self,None)
        self.parent = parent

        #Initialization of the plugin system
        init_plugin_system()
            
        #Got the enabled plugin
        self.settings =  QSettings()
        self.enabled_plugins = []
        for plugin in find_plugins():
            if bool(self.settings.value(plugin.__name__)):
                self.enabled_plugins.append(plugin)      

        self.findAndReplace = FindAndReplaceDlg()
        self.setupFileMenu()
        self.setupHelpMenu()
        self.setupEditor()

        try:
            self.setAttribute( Qt.WA_Maemo5AutoOrientation, True)
            self.setAttribute(Qt.WA_Maemo5StackedWindow, True)
            isMAEMO = True
        except:
            isMAEMO = False

        #Resize window if not maemo
        if not isMAEMO:
            self.resize(800, 600)
            
        self.area =  QScrollArea(self)
        try:
            scroller = self.area.property("kineticScroller") #.toPyObject()
            scroller.setEnabled(True)
        except:
            scroller = None
            
        #speed hack
        self.editor.scroller = scroller
        self.editor.area = self.area
        self.area.setWidget(self.editor)
        self.area.setWidgetResizable(True)
#        self.area.takeWidget()
        
#        self.setCentralWidget(self.editor)
        self.setCentralWidget(self.area)


    def fileSave(self):
        try:
            self.editor.save()
        except (IOError, OSError), e:
             QMessageBox.warning(self, "KhtEditor -- Save Error",
                    "Failed to save %s: %s" % (self.filename, e))


    def saveAsFile(self):
        filename =  QFileDialog.getSaveFileName(self,
                        "KhtEditor -- Save File As",
                        self.editor.filename, u'Python file(*.py);;'  
                                            + u'Text file(*.txt);;' 
                                            + u'C File(*.c);;' 
                                            + u'C++ File(*.cpp)')
        if not (filename == ''):
            self.editor.filename = filename
            self.setWindowTitle( QFileInfo(filename).fileName())
            self.fileSave()
        return filename


    def openFile(self, path=''):
        filename =  QFileDialog.getOpenFileName(self,
                            "KhtEditor -- Open File",path)
        if not (filename == ''):
            self.loadFile(filename)
        return filename


    def loadFile(self, filename):
        self.editor.filename = filename
        try:
            self.editor.load()
#             QTimer.singleShot(100, self.editor.load)
            self.setWindowTitle( QFileInfo(self.editor.filename).fileName())
#             QTimer.singleShot(100, self.loadHighlighter)
            self.loadHighlighter(filename)
        except (IOError, OSError), e:
             QMessageBox.warning(self, "KhtEditor -- Load Error",
                    "Failed to load %s: %s" % (filename, e))

    def setupEditor(self):
        font =  QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(12)

        self.editor = editor.KhtTextEdit(self)
        self.editor.setFont(font)
        #self.editor_frame = editor_frame.Frame(self.editor)
        self.setupToolBar()
#        self.language = self.detectLanguage()
#        self.loadHilighter()
        self.editor.document().modificationChanged.connect(self.do_documentChanged)

    def loadHighlighter(self,filename=None):
        global isMAEMO
        filename = self.editor.filename
        language = self.detectLanguage(filename)
        #Return None if language not yet implemented natively in KhtEditor
        if language == 'python':
            from syntax.python_highlighter import Highlighter
            if isMAEMO:
                self.setAttribute( Qt.WA_Maemo5ShowProgressIndicator,True)
            QApplication.processEvents()
            self.highlighter = Highlighter(self.editor.document())
            QApplication.processEvents()
            if isMAEMO:
                self.setAttribute( Qt.WA_Maemo5ShowProgressIndicator,False)
        elif (language != None) and (language != 'None'):
            from syntax.generic_highlighter import Highlighter
            if isMAEMO:
                self.setAttribute( Qt.WA_Maemo5ShowProgressIndicator,True)
            QApplication.processEvents()
            self.highlighter = Highlighter(self.editor.document(),language)
            QApplication.processEvents()
            if isMAEMO:
                self.setAttribute( Qt.WA_Maemo5ShowProgressIndicator,False)            
        else:
            from syntax import pygments_highlighter
            if isMAEMO:
                self.setAttribute( Qt.WA_Maemo5ShowProgressIndicator,True)
            QApplication.processEvents()
            self.highlighter = pygments_highlighter.Highlighter(self.editor.document(),str(filename))
            QApplication.processEvents()
            if isMAEMO:
                self.setAttribute( Qt.WA_Maemo5ShowProgressIndicator,False)            

    
    def detectLanguage(self,filename):
        for extension,lang in LANGUAGES:
            if filename.endswith(extension.lower()):
                 return lang
        return None
            
        return language
        
    def setupToolBar(self):
        self.toolbar = self.addToolBar('Toolbar')

        commentIcon =  QIcon.fromTheme("general_tag")
        prefix = os.path.join(os.path.dirname(__file__),'icons')
        indentIcon =  QIcon(os.path.join(prefix,'tb_indent.png'))

        unindentIcon =  QIcon(os.path.join(prefix,'tb_unindent.png'))
        saveIcon =  QIcon.fromTheme("notes_save")
        fullscreenIcon =  QIcon.fromTheme("general_fullsize")
        executeIcon =  QIcon.fromTheme("general_forward")
        findIcon =  QIcon.fromTheme("general_search")

        self.lineCount =  QLabel('L.1 C.1')
        self.toolbar.addWidget(self.lineCount)
        self.editor.cursorPositionChanged.connect(self.lineCountUpdate)
        self.tb_comment =  QAction(commentIcon, 'Comment', self)
        self.tb_comment.triggered.connect(self.editor.comment)
        self.toolbar.addAction(self.tb_comment)
        self.tb_indent =  QAction(indentIcon, 'Indent', self)
        self.tb_indent.setShortcut('Ctrl+I')
        self.tb_indent.triggered.connect( self.editor.indent)
        self.toolbar.addAction(self.tb_indent)
        self.tb_unindent =  QAction(unindentIcon, 'Unindent', self)
        self.tb_unindent.setShortcut('Ctrl+U')
        self.tb_unindent.triggered.connect(self.editor.unindent)
        self.toolbar.addAction(self.tb_unindent)
        self.tb_find =  QAction(findIcon, 'Find', self)
        self.tb_find.setShortcut('Ctrl+F')
        self.tb_find.triggered.connect(self.do_find)
        self.toolbar.addAction(self.tb_find)
        self.tb_save =  QAction(saveIcon, 'Save', self)
        self.tb_save.setShortcut('Ctrl+S')
        self.tb_save.triggered.connect(self.fileSave)
        self.toolbar.addAction(self.tb_save)
        self.tb_execute =  QAction(executeIcon, 'Execute', self)
        self.tb_execute.setShortcut('Ctrl+E')
        self.tb_execute.triggered.connect(self.do_execute)
        self.toolbar.addAction(self.tb_execute)
        self.tb_fullscreen =  QAction(fullscreenIcon, 'Fullscreen', self)
        self.tb_fullscreen.triggered.connect(self.do_fullscreen)
        self.toolbar.addAction(self.tb_fullscreen)

        #Actions not in toolbar
        self.tb_duplicate =  QAction('Duplicate', self)
        self.tb_duplicate.setShortcut('Ctrl+D')
        self.tb_duplicate.triggered.connect(self.editor.duplicate)
        self.addAction(self.tb_duplicate)
        self.tb_findagain =  QAction('Find Again', self)
        self.tb_findagain.setShortcut('Ctrl+G')
        self.tb_findagain.triggered.connect(self.findAndReplace.findClicked)
        self.addAction(self.tb_findagain)

        #Hook for plugins to add buttons :
        for plugin in filter_plugins_by_capability('toolbarHook',self.enabled_plugins):
            print 'Found 1 Plugin for toolbarHook'
            plg = plugin()
            plg.do_toolbarHook(self)

    def setupFileMenu(self):
        fileMenu =  QMenu(self.tr("&File"), self)
        self.menuBar().addMenu(fileMenu)

        fileMenu.addAction(self.tr("New..."), self.parent.newFile,
                 QKeySequence(self.tr("Ctrl+N", "New")))
        fileMenu.addAction(self.tr("Open..."), self.parent.openFile,
                 QKeySequence(self.tr("Ctrl+O", "Open")))
        fileMenu.addAction(self.tr("Save As"), self.saveAsFile,
                 QKeySequence(self.tr("Ctrl+Maj+S", "Save As")))

    def setupHelpMenu(self):
        helpMenu =  QMenu(self.tr("&Help"), self)
        self.menuBar().addMenu(helpMenu)

        helpMenu.addAction(self.tr("&About"), self.do_about)

    def do_about(self):
        self.parent.about(self)

    def do_gotoLine(self, line):
        print 'goto line:'+str(line)
        self.editor.gotoLine(line)

    def do_find(self):
        self.findAndReplace.find.connect(self.editor.find)
        self.findAndReplace.replace.connect(self.editor.replace)
        self.findAndReplace.replaceAll(self.editor.replace_all)
        self.findAndReplace.show()

    def do_execute(self):
        print "execute"
        #ask for save if unsaved
        self.fileSave()

        if self.editor.filename != None:
          fileHandle = open('/tmp/khteditor.tmp', 'wb')
          fileHandle.write('#!/bin/sh\n')
          fileHandle.write('cd '+os.path.dirname(unicode(self.editor.filename).encode('utf-8'))+' \n')
          language = self.detectLanguage(self.editor.filename)
          #Crappy way to handle that
          if language == 'python':
            fileHandle.write("python \'"+unicode(self.editor.filename).encode('utf-8') + "\'\n")
          elif language == 'qml':
            fileHandle.write("/opt/qt4-maemo5/bin/qmlviewer \'"+unicode(self.editor.filename).encode('utf-8') + "\' -fullscreen\n")             
          elif language != None:
            fileHandle.write(language+" \'"+unicode(self.editor.filename).encode('utf-8') + "\' \n")
          else:
            fileHandle.write("\'"+unicode(self.editor.filename).encode('utf-8') + "\' \n")
          fileHandle.write('read -p "Press ENTER to continue ..." foo')
          fileHandle.write('\nexit')
          fileHandle.close()
          commands.getoutput("chmod 777 /tmp/khteditor.tmp")
          Popen('/usr/bin/osso-xterm /tmp/khteditor.tmp',shell=True,stdout=None)

    def lineCountUpdate(self):
        cursor = self.editor.textCursor()
        self.lineCount.setText("L.%d C.%d" % (cursor.blockNumber()+1,
                                            cursor.columnNumber()+1))

    def closeEvent(self,event):
        self.editor.closeEvent(event)

    def do_fullscreen(self):
        if self.isFullScreen():
            self.showMaximized()
        else:
            self.showFullScreen()

    def do_documentChanged(self,changed):
        if changed == True:
            self.setWindowTitle('*'+ QFileInfo(self.editor.filename).fileName())
        else:
            self.setWindowTitle( QFileInfo(self.editor.filename).fileName())
