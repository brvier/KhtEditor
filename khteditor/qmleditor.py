from PySide.QtDeclarative import QDeclarativeItem
from PySide.QtGui import QGraphicsProxyWidget, QGraphicsItem
from PySide.QtCore import QSize, Slot, Property, Signal
from editor import KhtTextEditor
						
class QmlTextEditor(QDeclarativeItem):
    heightChanged = Signal()
    widthChanged = Signal()
    
    def __init__(self, parent=None):
        QDeclarativeItem.__init__(self, parent)
        
        self.widget = KhtTextEditor(inQML=True)
        self.proxy = QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.widget)
        self.proxy.setPos(0,0)
        self.setFlag(QGraphicsItem.ItemHasNoContents, False)
        self.widget.setPlainText('test\n'*200)
        self.widget.sizeChanged.connect(self.sizeChanged)
        self._width = self.widget.width()       
        self._height = self.widget.height()
        print 'Debug:', self._width,':',self._height

    def getWidth(self):
        return self._width
        
    def setWidth(self,width):
        if width != self._width:
            self._width = width
            self.widthChanged.emit()
            
    def getHeight(self):
        return self._height
        
    def setHeight(self,height):
        if height != self._height:
            self._height = height
            self.heightChanged.emit()
            
    width = Property(int,getWidth, setWidth, notify=widthChanged)
    height = Property(int, getHeight, setHeight, notify=heightChanged)
    
    @Slot(QSize)
    def sizeChanged(self,size):
        self.setWidth(size.width())
        self.setHeight(size.height())