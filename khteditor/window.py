#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Benoît HERVIER
# Licenced under GPLv3

from PySide.QtCore import Qt, QSettings, Slot, Signal
from PySide.QtGui import QMainWindow, \
                         QAction, QIcon, QScrollArea, QFileDialog, \
                         QMessageBox, QMenu, QToolButton, \
                         QFrame #, QMenu, QWidget

#Try import QtMaemo5
try:
    from PySide import QtMaemo5
    print '%s loaded' % QtMaemo5.__name__
    from PySide.QtGui import QAbstractKineticScroller
except:
    print 'PySide QtMaemo5 cannot be loaded'

import os.path

from plugins.plugins_api import filter_plugins_by_capability

prefix = os.path.join(os.path.dirname(__file__),'icons')

TOOLBAR_BUTTONS = (
        {'Name':'Errors','DefaultPrefs':True,'Icon':'','Visible':False, },
        {'Name':'Line_Number','DefaultPrefs':True,'Visible':True, 'DefaultValue':'L.1 C.1'},
        {'Name':'Comment','DefaultPrefs':True,'Icon':'general_tag','Shortcut':'Ctrl+H',},
        {'Name':'Duplicate','DefaultPrefs':False,'Icon':'','Shortcut':'Ctrl+D',},
        {'Name':'Indent','DefaultPrefs':True,'Icon':os.path.join(prefix,'tb_indent.png'),'Shortcut':'Ctrl+I'},
        {'Name':'Unindent','DefaultPrefs':True,'Icon':os.path.join(prefix,'tb_unindent.png'),'Shortcut':'Ctrl+U'},
        {'Name':'Search','DefaultPrefs':True,'Icon':'general_search','Shortcut':'Ctrl+F'},
        {'Name':'Open','DefaultPrefs':True,'Icon':'','Shortcut':'Ctrl+O'},
        {'Name':'Recent_Files','DefaultPrefs':False,'Icon':'','Shortcut':'Ctrl+R'},
        {'Name':'Save','DefaultPrefs':True,'Icon':'notes_save','Shortcut':'Ctrl+S'},
        {'Name':'Close','DefaultPrefs':True,'Icon':'','Shortcut':'Ctrl+W'},
        {'Name':'Execute','DefaultPrefs':True,'Icon':'general_forward','Shortcut':'Ctrl+E'},
        {'Name':'Fullscreen','DefaultPrefs':True,'Icon':'general_fullsize','Shortcut':'Ctrl+M'},
        {'Name':'Plugins','DefaultPrefs':True,},
                  )

from editor import KhtTextEditor

class KhtWindow(QMainWindow):
    closed = Signal()
    tb_openFile = Signal(unicode) #unicode : current filepath

    def __init__(self,parent=None, enabled_plugins=[]):
        QMainWindow.__init__(self,parent)

        #Try to set Maemo Properties
        try:
            self.setAttribute(Qt.WA_Maemo5AutoOrientation, True)
            self.setAttribute(Qt.WA_Maemo5StackedWindow, True)
        except:
            #Resize window if not maemo
            self.resize(1024, 800)

        #Preload settings
        self.settings = QSettings()

        self.aboutWin = None
        self.prefsWin = None

        #Start Construction of the GUI
        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.setMovable (True)
        self.toolbar.setAllowedAreas(Qt.BottomToolBarArea)
        self.action_widgets = {}
        for tb_button in TOOLBAR_BUTTONS:
            icon = None

             #Specific Toolbar action for Plugins menu
            if tb_button['Name'] == 'Plugins':
                self.tb_plugin_menu = QMenu(self)
                self.tb_plugin_button = QToolButton(self)
                self.tb_plugin_button.setText('Plugins')
                self.tb_plugin_button.setMenu(self.tb_plugin_menu)
                self.tb_plugin_button.setPopupMode(QToolButton.InstantPopup)
                self.tb_plugin_button.setCheckable(False)
                self.toolbar.addWidget(self.tb_plugin_button)

                #Hook for plugins to add buttons in combo box:
                for plugin in filter_plugins_by_capability('toolbarHook',enabled_plugins):
                    print 'Found 1 Plugin for toolbarHook'
                    plugin.do_toolbarHook(self.tb_plugin_menu)

            #Other Toolbar Action
            else:

                if 'Icon' in tb_button:
                    if tb_button['Icon']:
                        path = os.path.join(os.path.dirname(__file__),'icons',tb_button['Icon'])
                        if os.path.exists(path):
                            icon = QIcon(os.path.join(os.path.dirname(__file__),'icons',tb_button['Icon']))
                        else:
                            icon = QIcon.fromTheme(tb_button['Icon'])
                if icon:
                    action = QAction(icon, tb_button['Name'], self)
                else:
                    action = QAction(tb_button['Name'], self)


                if 'Visible' in tb_button:
                    action.setVisible(tb_button['Visible'])

                if 'DefaultValue' in tb_button:
                    action.setText(tb_button['DefaultValue'])

                if 'Shortcut' in tb_button:
                    action.setShortcut(tb_button['Shortcut'])
                action.triggered.connect(self.toolbarTriggered)

                #Add action to toolbar if activated else to win to keep shortcut
                if self.settings.contains(tb_button['Name']):
                    if str(self.settings.value(tb_button['Name'])) == '2':
                        self.toolbar.addAction(action)
                    else:
                        self.addAction(action)
                else:
                    self.addAction(action)

                self.action_widgets[tb_button['Name']] = action

        #Add a menu
        self.menuBar = self.menuBar()
        self.menu = self.menuBar.addMenu(self.tr('&Menu'))
        self.menu.addAction(self.tr('&Open'), self.openFile)
        self.menu.addAction(self.tr('&Open Recent'), self.showRecent)
        self.menu.addAction(self.tr('&Save as'), self.saveFile)
        self.menu.addAction(self.tr('&Save as'), self.saveAsFile)
        self.menu.addAction(self.tr('&About'), self.showAbout)
        self.menu.addAction(self.tr('&Preferences'), self.showPrefs)

        self.area =  QScrollArea(self)
        try:
            scroller = self.area.property("kineticScroller")
            if scroller == None:
                raise StandardError("No QtMaemo5")
            self.editor = KhtTextEditor(self.area, scroller=scroller)
            scroller.setEnabled(True)
            scroller.setOvershootPolicy(QAbstractKineticScroller.OvershootAlwaysOff)
            self.area.setWidgetResizable(True)
            self.area.setFrameStyle(QFrame.NoFrame)
            self.area.setViewportMargins(0,0,0,0)
            self.area.setContentsMargins(0,0,0,0)
            self.area.setWidget(self.editor)
            self.setCentralWidget(self.area)
        except Exception, err:
            print err
            self.editor = KhtTextEditor(self,scroller=None)
            self.area.close()
            self.area.destroy()
            del self.area

            self.setCentralWidget(self.editor)


        self.editor.showProgress.connect(self.showProgress)
        #self.editor.enabled_plugins = enabled_plugins
        #self.editor.filepathChanged.connect(self.changeWindowTitle)
        self.editor.modificationChanged.connect(self.modificationWindowTitle)
        self.editor.cursorPositionChanged.connect(self.curPositionChanged)
        self.editor.documentErrorsChanged.connect(self.showErrorsTB)
        self.show()

    @Slot()
    def showErrorsTB(self):
        if hasattr(self.editor.document(),'errors'):
            show = len(self.editor.document().errors) > 0
        else:
            show = False
        self.action_widgets['Errors'].setVisible(show)

    @Slot()
    def curPositionChanged(self):
        cursor = self.editor.textCursor()
        self.action_widgets['Line_Number'].setText("L.%d C.%d" % (cursor.blockNumber()+1,
                                            cursor.columnNumber()+1))

    @Slot(bool)
    def modificationWindowTitle(self, changed):
        self.setWindowTitle(('*' if changed else '') + os.path.basename(self.editor.getFilePath()))

    @Slot(unicode)
    def changeWindowTitle(self, filepath):
        self.setWindowTitle(os.path.basename(filepath))

    @Slot()
    def closeEvent(self,event):
        """Catch the close event and ask to save if document is modified"""
        answer = self.editor.document().isModified() and \
        QMessageBox.question(self,
               "KhtEditor - Unsaved Changes",
               "Save unsaved changes in %s?" % self.editor._filepath,
               QMessageBox.Yes| QMessageBox.No| QMessageBox.Close)
        if answer ==  QMessageBox.Yes:
            try:
                self.editor.save()
                self.closed.emit()
                event.accept()
            except (IOError, OSError), ioError:
                QMessageBox.warning(self, "KhtEditor -- Save Error",
                        "Failed to save %s: %s" % (self.editor._filepath, ioError))
                event.ignore()
        elif answer ==  QMessageBox.Close:
            return event.ignore()
        else:
            self.closed.emit()
            return event.accept()

    @Slot()
    def showAbout(self):
        from about import QAboutWin
        if not self.aboutWin:
            self.aboutWin = QAboutWin(self)
        self.aboutWin.show()

    @Slot()
    def showPrefs(self):
        from settings import KhtESettings
        if not self.prefsWin:
            self.prefsWin = KhtESettings(self)
        self.prefsWin.show()

    @Slot(bool)
    def showProgress(self,show):
        try:
            self.setAttribute(Qt.WA_Maemo5ShowProgressIndicator, show)
        except AttributeError:
            print 'QtMaemo5 not available'

    @Slot()
    def showRecent(self):
        print 'Show recents not implemented yet'
        
    def saveAsFile(self):
        filename, ok =  QFileDialog.getSaveFileName(self,
                        "KhtEditor -- Save File As",
        self.editor._filepath, u'Python file(*.py);;'
                                            + u'Text file(*.txt);;'
                                            + u'QML file(*.qml);;'
                                            + u'C File(*.c);;'
                                            + u'C++ File(*.cpp)')
        if not (filename == ''):
            self.editor.setFilePath(filename)
            #self.setWindowTitle( QFileInfo(self.editor._filepath).fileName())
            try:
                self.saveFile()
            except (IOError, OSError), ioError:
                 QMessageBox.warning(self, "KhtEditor -- Save Error",
                        "Failed to save %s: %s" % (self.editor.filename, ioError))

    def saveFile(self):
        if os.path.basename(self.editor._filepath) == "Unnamed":
            self.saveAsFile()
        else:
            try:
                self.editor.save()
            except (IOError, OSError), ioError:
                 QMessageBox.warning(self, "KhtEditor -- Save Error",
                        "Failed to save %s: %s" % (self.editor.filename, ioError))

    @Slot()
    def executeFile(self):
        print 'Not yet implemented'
        
    @Slot()
    def openFile(self):
        self.tb_openFile.emit(self.editor._filepath)

    @Slot()
    def toolbarTriggered(self):
        action = self.sender().text()
        if action == 'Open':
            self.openFile()
        elif action == 'Save':
            self.saveFile()
        elif action == 'Close':
            self.close()
        elif action == 'Indent':
            self.editor.indent()
        elif action == 'Unindent':
            self.editor.unindent()
        elif action == 'Comment':
            self.editor.comment()
        elif action == 'Duplicate':
            self.editor.duplicate()
        elif action == 'Execute':
            self.editor.execute()
        elif action == 'Fullscreen':
            if self.isFullScreen():
                self.showMaximized()
            else:
                self.showFullScreen()
        else:
            print '%s not implemented' % action
