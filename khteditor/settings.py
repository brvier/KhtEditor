from PyQt4.QtGui import QMainWindow, \
    QSizePolicy, \
    QSpinBox, \
    QApplication, \
    QCheckBox, \
    QFontComboBox, \
    QGridLayout, \
    QWidget, \
    QLabel, \
    QScrollArea

from PyQt4.QtCore import QSettings, \
    Qt
    
from plugins.plugins_api import init_plugin_system, filter_plugins_by_capability, find_plugins
import os
import sys

class KhtSettings(QMainWindow):
    def __init__(self, parent=None):
        global isMAEMO
        QMainWindow.__init__(self,parent)
        self.parent = parent

        try:
            self.setAttribute(Qt.WA_Maemo5AutoOrientation, True)
            self.setAttribute(Qt.WA_Maemo5StackedWindow, True)
            isMAEMO = True
        except:
            isMAEMO = False
        self.setWindowTitle("KhtEditor Prefs")

        #Resize window if not maemo
        if not isMAEMO:
            self.resize(800, 600)
            
        self.settings = QSettings()
        
        self.setupGUI()
        self.loadPrefs()
        
    def loadPrefs(self):
        for checkBox in self.plugins_widgets :            
            if self.settings.value(checkBox.text().split(' ')[0])!=None:        
                checkBox.setCheckState(int(self.settings.value(checkBox.text().split(' ')[0])))
        if self.settings.value('FontName') :
            self.fontName.setCurrentFont(self.settings.value('FontName'))
        if self.settings.value("FontSize"):
            self.fontSize.setValue(int(self.settings.value("FontSize")))    
        if self.settings.value('WrapLine'):        
            self.wrapLine.setCheckState(int(self.settings.value('WrapLine')))

    def savePrefs(self):
        for checkBox in self.plugins_widgets :
            self.settings.setValue(checkBox.text().split(' ')[0],checkBox.checkState())
        self.settings.setValue('FontName',self.fontName.currentFont())
        self.settings.setValue('FontSize',self.fontSize.value())
        self.settings.setValue('WrapLine',self.wrapLine.checkState())
            
    def closeEvent(self,widget,*args):
        self.savePrefs()
                     
    def setupGUI(self):
        global isMAEMO
        
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)

        self.aWidget = QWidget(self.scrollArea)
        self._main_layout = QGridLayout(self.aWidget)
        self.aWidget.setMinimumSize(480,800)
        self.aWidget.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scrollArea.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scrollArea.setWidget(self.aWidget)
        if isMAEMO:
            scroller = self.scrollArea.property("kineticScroller") #.toPyObject()
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

        self.plugins_widgets = []
        for plugin in find_plugins():
            aCheckBox = QCheckBox(plugin.__name__+' '+plugin.__version__)
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

        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setOrganizationName("Khertan Software")
    app.setOrganizationDomain("khertan.net")
    app.setApplicationName("KhtEditor")
    
    khtsettings = KhtSettings()
    khtsettings.show()
    sys.exit(app.exec_())
