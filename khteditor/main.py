#/use/bin/python

from PySide.QtGui import QApplication, QDirModel
from PySide.QtCore import QObject, QUrl
from PySide import QtDeclarative

import sys
import os.path

from qmleditor import QmlTextEditor
from plugins.plugins_api import init_plugin_system
 
class KhtEditor(QApplication):
    def __init__(self):

        QApplication.__init__(self,sys.argv)
        self.setOrganizationName("Khertan Software")
        self.setOrganizationDomain("khertan.net")
        self.setApplicationName("KhtEditor")

        QtDeclarative.qmlRegisterType(QmlTextEditor,'net.khertan.qmlcomponents',1,0,'QmlTextEditor')

        #Initialization of the plugin system
        init_plugin_system()        
                    
        self.dirModel = QDirModel()
        self.view = QtDeclarative.QDeclarativeView()
        self.view.rootContext().setContextProperty("dirModel", self.dirModel)
        self.view.setSource(QUrl.fromLocalFile("qml3/main.qml"))
        self.view.showFullScreen()


if __name__ == '__main__':
    sys.exit(KhtEditor().exec_())
