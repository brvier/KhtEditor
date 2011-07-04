#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Benoît HERVIER
# Licenced under GPLv3

from PySide.QtCore import QSettings, Qt

from PySide.QtGui import QMainWindow, \
    QSizePolicy, QSpinBox, QApplication, \
    QCheckBox, QFontComboBox, \
    QGridLayout, QWidget, QLabel, \
    QScrollArea, QComboBox

from plugins.plugins_api import init_plugin_system, find_plugins
import sys

from window import TOOLBAR_BUTTONS
from styles import STYLES

class KhtESettings(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)
        self.parent = parent

        self.setWindowTitle("KhtEditor Prefs")

        try:
            self.setAttribute(Qt.WA_Maemo5AutoOrientation, True)
            self.setAttribute(Qt.WA_Maemo5StackedWindow, True)
        except:
            #Resize window if not maemo
            self.resize(1024, 800)

        self.settings = QSettings()

        self.setupGUI()
        self.loadPrefs()

    def loadCheckBox(self,name,widget,default=False):
        #check default
        if not self.settings.contains(name):
            if default:
                value = '2'
            else:
                value = '0'
        else:
            value = self.settings.value(name)

        if str(value) == '2':
            widget.setCheckState(Qt.CheckState.Checked)
        else:
            widget.setCheckState(Qt.CheckState.Unchecked)

    def loadPrefs(self):
        #Load Plugin Prefs
        for checkBox in self.plugins_widgets :
            self.loadCheckBox(checkBox.text().split(' ')[0],checkBox,False)

        #Load font and size preferences
        if self.settings.value('FontName') :
            self.fontName.setCurrentFont(self.settings.value('FontName'))
        if self.settings.value("FontSize"):
            self.fontSize.setValue(int(self.settings.value("FontSize")))

        #Load toolbar buttons
        for tb_button in TOOLBAR_BUTTONS:
            self.loadCheckBox(tb_button['Name'],\
                              self.toolbar_button_widgets[tb_button['Name']],\
                              tb_button['DefaultPrefs'])
        #Load other prefs
        self.loadCheckBox('WrapLine',self.wrapLine,False)
        self.loadCheckBox('qt18720',self.qt18720,False)

        #Load Theme
        if self.settings.contains('theme'):
            if not self.settings.value('theme') in STYLES:
                self.settings.setValue('theme', 'default')
        else:
            self.settings.setValue('theme', 'default')
        self.theme_value.setCurrentIndex(self.theme_value.findText(self.settings.value('theme')))

    def savePrefs(self):
        #Save Plugins
        for checkBox in self.plugins_widgets :
            self.settings.setValue(checkBox.text().split(' ')[0],checkBox.checkState())
        #Save ToolBar Button
        for tb_button in TOOLBAR_BUTTONS:
            self.settings.setValue(tb_button['Name'],\
                    self.toolbar_button_widgets[tb_button['Name']].checkState())
        self.settings.setValue('FontName',self.fontName.currentFont())
        self.settings.setValue('FontSize',self.fontSize.value())
        self.settings.setValue('WrapLine',self.wrapLine.checkState())
        self.settings.setValue('qt18720',self.qt18720.checkState())
        #Save theme
        self.settings.setValue('theme',self.theme_value.currentText())

    def closeEvent(self,widget,*args):
        self.savePrefs()

    def setupGUI(self):
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)

        self.aWidget = QWidget(self.scrollArea)
        self._main_layout = QGridLayout(self.aWidget)
        self.aWidget.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scrollArea.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scrollArea.setWidget(self.aWidget)
        try:
            scroller = self.scrollArea.property("kineticScroller") #.toPyObject()
            scroller.setEnabled(True)
        except:
            pass
        gridIndex = 0

        self._main_layout.addWidget(QLabel('Font :'),gridIndex,0)
        gridIndex += 1

        self.fontName = QFontComboBox()
        self._main_layout.addWidget(self.fontName,gridIndex,1)
        gridIndex += 1
        self.fontSize = QSpinBox()
        self._main_layout.addWidget(self.fontSize,gridIndex,1)
        gridIndex += 1

        #Theme
        self._main_layout.addWidget(QLabel('Coloration Style :'),gridIndex,0)
        self.theme_value = QComboBox()
        self._main_layout.addWidget(self.theme_value, gridIndex, 1)
        for theme in STYLES:
            self.theme_value.addItem(theme)
        gridIndex += 1

        #Toolbar
        self._main_layout.addWidget(QLabel('Toolbar Buttons :'),gridIndex,0)
        gridIndex += 1

        self.toolbar_button_widgets = {}
        for tb_button in TOOLBAR_BUTTONS:
            aCheckBox = QCheckBox(tb_button['Name'].replace(' ','_'))
            self.toolbar_button_widgets[tb_button['Name']]=aCheckBox
            self._main_layout.addWidget(aCheckBox,gridIndex,1)
            gridIndex += 1

        self._main_layout.addWidget(QLabel('Plugins :'),gridIndex,0)
        gridIndex += 1

        init_plugin_system()

        self.plugins_widgets = []
        for plugin in find_plugins():
            aCheckBox = QCheckBox(plugin.__name__+' '+plugin.__version__)
            self.plugins_widgets.append(aCheckBox)
            self._main_layout.addWidget(aCheckBox,gridIndex,1)
            gridIndex += 1

        self._main_layout.addWidget(QLabel('Others preferences :'),gridIndex,0)
        gridIndex += 1
        self.wrapLine = QCheckBox('Wrap Lines')
        self._main_layout.addWidget(self.wrapLine,gridIndex,1)
        gridIndex += 1
        self.qt18720 = QCheckBox('Work Arround QTBUG-18720')
        self._main_layout.addWidget(self.qt18720,gridIndex,1)
        gridIndex += 1

        self.aWidget.resize(-1,-1)
        self.aWidget.setLayout(self._main_layout)
        self.setCentralWidget(self.scrollArea)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setOrganizationName("Khertan Software")
    app.setOrganizationDomain("khertan.net")
    app.setApplicationName("KhtEditor")

    khtsettings = KhtESettings()
    khtsettings.show()
    sys.exit(app.exec_())
