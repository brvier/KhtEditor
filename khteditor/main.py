#/use/bin/python

from PySide.QtGui import QApplication
from PySide.QtCore import QObject
from PySide import QtDeclarative

import sys
import os.path
#import time
#import random

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
                    
        self.views = []

        for arg in sys.argv[1:]:
            if os.path.exists(arg):
                self.open_view(filepath=arg)

        if len(self.views)==0:
            self.open_view()
            
    def open_view(self,filepath=None):
        view = QtDeclarative.QDeclarativeView()
        view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        view.setSource('qml/main.qml')
        if filepath:
            view.setWindowTitle(os.path.basename(filepath))
            root = view.rootObject()
            root.setProperty('filepath',os.path.abspath(filepath))
            root.setProperty('filename',os.path.basename(filepath))
            #print root, dir(root)
            #mainPages = root.findChildren(QObject,"mainPage")
            #mainPages[0].setProperty('filepath',os.path.abspath(filepath))

        else:
            view.setWindowTitle('Untitled')
        view.showFullScreen()
        self.views.append(view)
        

if __name__ == '__main__':
    sys.exit(KhtEditor().exec_())
