from PyQt4.QtGui import *
from PyQt4.QtCore import *
import plugins_api
import os

class KhtSettings(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)
        self.parent = parent

        self.setAttribute(Qt.WA_Maemo5AutoOrientation, True)
        self.setAttribute(Qt.WA_Maemo5StackedWindow, True)
        self.setWindowTitle("KhtEditor Prefs")

        self.settings = QSettings()
        
        self.setupGUI()
        self.loadPrefs()
        
    def loadPrefs(self):
        for checkBox in self.plugins_widgets :
            checkBox.setCheckState(self.settings.value(checkBox.text()).toInt()[0])


    def savePrefs(self):
        for checkBox in self.plugins_widgets :
            self.settings.setValue(checkBox.text(),checkBox.checkState())
            
    def closeEvent(self,widget,*args):
        self.savePrefs()
                     
    def setupGUI(self):
        self.aWidget = QWidget()
        self._main_layout = QGridLayout(self.aWidget)

        gridIndex = 0
        self._main_layout.addWidget(QLabel('Plugins :'),gridIndex,0)
        gridIndex += 1
        
        plugins = plugins_api.discover_plugin_in_paths()        
        self.plugins_widgets = []
        for plugin_name in plugins:        
            aCheckBox = QCheckBox(plugin_name)
            self.plugins_widgets.append(aCheckBox)
            self._main_layout.addWidget(aCheckBox,gridIndex,0)
            gridIndex += 1
                            
        self.aWidget.setLayout(self._main_layout)
        self.setCentralWidget(self.aWidget)