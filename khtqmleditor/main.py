from PySide import QtGui
from PySide import QtCore
from PySide import QtDeclarative

import sys
import time
import random


#http://qt.gitorious.org/pyside/pyside-examples/trees/master/examples/declarative/extending

from editor import KhtTextEditor, QmlTextEditor

#class KhtProxyTextEditor(QtDeclarative.QDeclarativeItem):
#    #onKeyPressed = QtCore.Signal(QtCore.QEvent)
#    
#    def __init__(self,parent=None):
#        QtDeclarative.QDeclarativeItem.__init__(self,parent)
#        self.editor = KhtTextEditor()



app = QtGui.QApplication(sys.argv)
app.setOrganizationName('Khertan Software')
app.setOrganizationDomain('khertan.net')
app.setApplicationName('KhtEditor')

#editor = KhtTextEditor()
QtDeclarative.qmlRegisterType(QmlTextEditor,'net.khertan.qmlcomponents',1,0,'KhtTextEditor')

view = QtDeclarative.QDeclarativeView()


view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
#view.rootContext().setContextProperty('listener', listener)
view.setSource(__file__.replace('.py', '.qml'))

view.showFullScreen()

app.exec_()
