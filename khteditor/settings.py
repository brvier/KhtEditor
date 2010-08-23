from PyQt4.QtGui import *
from PyQt4.QtCore import *
from plugins_api import init_plugin_system, filter_plugins_by_capability, find_plugins
import os
import sys

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
        if (self.settings.value('FontName').toPyObject()) != None:
            self.fontName.setCurrentFont(self.settings.value('FontName').toPyObject())
        self.fontSize.setValue(self.settings.value("FontSize").toInt()[0])        
        self.wrapLine.setCheckState(self.settings.value('WrapLine').toInt()[0])

    def savePrefs(self):
        for checkBox in self.plugins_widgets :
            self.settings.setValue(checkBox.text(),checkBox.checkState())
        self.settings.setValue('FontName',QVariant(self.fontName.currentFont()))
        self.settings.setValue('FontSize',QVariant(self.fontSize.value()))
        self.settings.setValue('WrapLine',self.wrapLine.checkState())
            
    def closeEvent(self,widget,*args):
        self.savePrefs()
                     
    def setupGUI(self):
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)

        self.aWidget = QWidget(self.scrollArea)
        self._main_layout = QGridLayout(self.aWidget)
        self.aWidget.setMinimumSize(480,800)
        self.aWidget.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scrollArea.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scrollArea.setWidget(self.aWidget)
        scroller = self.scrollArea.property("kineticScroller").toPyObject()
        scroller.setEnabled(True)

        gridIndex = 0

        self._main_layout.addWidget(QLabel('Font :'),gridIndex,0)
        gridIndex += 1
        
        self.fontName = QFontComboBox()
        self._main_layout.addWidget(self.fontName,gridIndex,0)
        gridIndex += 1        
        self.fontSize = QSpinBox()
        self._main_layout.addWidget(self.fontSize,gridIndex,0)
        gridIndex += 1        

        self._main_layout.addWidget(QLabel('Plugins :'),gridIndex,0)
        gridIndex += 1
        
        init_plugin_system()
#        plugins = 
#        plugins = plugins_api.discover_plugin_in_paths()
        self.plugins_widgets = []
        for plugin in find_plugins():
            aCheckBox = QCheckBox(plugin.__name__)
            self.plugins_widgets.append(aCheckBox)
            self._main_layout.addWidget(aCheckBox,gridIndex,0)
            gridIndex += 1

        self._main_layout.addWidget(QLabel('Others preferences :'),gridIndex,0)
        gridIndex += 1
        self.wrapLine = QCheckBox('Wrap Lines')
        self._main_layout.addWidget(self.wrapLine,gridIndex,0)
        gridIndex += 1

                            
        self.aWidget.setLayout(self._main_layout)
        self.setCentralWidget(self.scrollArea)

#        self.setCentralWidget(self.aWidget)
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setOrganizationName("Khertan Software")
    app.setOrganizationDomain("khertan.net")
    app.setApplicationName("KhtEditor")
    
    khtsettings = KhtSettings()
    khtsettings.show()
    sys.exit(app.exec_())
