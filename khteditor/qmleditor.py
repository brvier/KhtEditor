from PySide.QtDeclarative import QDeclarativeItem
from PySide.QtGui import QGraphicsProxyWidget, QGraphicsItem
from editor import KhtTextEditor
						
class QmlTextEditor(QDeclarativeItem):
    def __init__(self, parent=None):
        QDeclarativeItem.__init__(self, parent)
        
        self.widget = KhtTextEditor(inQML=True)
        self.proxy = QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.widget)
        self.proxy.setPos(0,0)
        self.setFlag(QGraphicsItem.ItemHasNoContents, False)
        self.widget.setEnabled(False)
        self.widget.setPlainText('test\n'*200)
#        self.widget.resize(850,850)
#        self.setKeepMouseGrab(True)