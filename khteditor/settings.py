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
        pass

    def savePrefs(self):
        pass
        
    def closeEvent(self,widget,*args):
        self.savePrefs()
                     
    def setupGUI(self):
        self.aWidget = QWidget()
        self._main_layout = QGridLayout(self.aWidget)

        gridIndex = 0
        self._main_layout.addWidget(QLabel('Plugins :'),gridIndex,0)
        gridIndex += 1
        
        for plugin_name in findPlugins():        
            self.login_value = QLineEdit('PluginName')
            self._main_layout.addWidget(self.login_value,gridIndex,1)
            gridIndex += 1
                            
        self.aWidget.setLayout(self._main_layout)
        self.setCentralWidget(self.aWidget)