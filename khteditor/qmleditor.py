from PySide.QtDeclarative import QDeclarativeItem
from PySide.QtGui import QGraphicsProxyWidget, QGraphicsItem
from PySide.QtCore import QSize, Slot, Property, Signal
from editor import KhtTextEditor
						
class QmlTextEditor(QDeclarativeItem):
    heightChanged = Signal()
    widthChanged = Signal()
    filepathChanged = Signal()
    modificationChanged = Signal()
    
    def __init__(self, parent=None):
        QDeclarativeItem.__init__(self, parent)

        self.widget = KhtTextEditor(inQML=True)
        self.proxy = QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.widget)
        self.proxy.setPos(0,0)
        self.setFlag(QGraphicsItem.ItemHasNoContents, False)
        self.widget.sizeChanged.connect(self.sizeChanged)
        self._width = self.widget.width()       
        self._height = self.widget.height()
        print 'Debug: Initial size:',self._width,':',self._height
        self.widget.filepathChanged.connect(self.filepathChanged)
        self._modification = False
        self.widget.modificationChanged.connect(self.setModificationChanged)

    @Slot()
    def indent(self):
        self.widget.indent()

    @Slot()
    def unindent(self):
        self.widget.unindent()
        
    @Slot()
    def comment(self):
        self.widget.comment()

    @Slot()
    def save(self):
        self.widget.save()

    @Slot()
    def execute(self):
        self.widget.execute()
                
    @Slot(QSize)
    def sizeChanged(self,size):
        self.setWidth(size.width())
        self.setHeight(size.height())
        
    def getModificationChanged(self): return self._modification
    def setModificationChanged(self, changed):
        if changed != self._modification:
            print 'Changed:',self._modification
            self._modification = changed
            self.modificationChanged.emit()

    def getFilepath(self): return self.widget.getFilePath()        
    def setFilepath(self,filepath):
        if filepath:
            if self.widget.getFilePath() != filepath:
                self.widget.setFilePath(filepath)
                self.widget.load()
                self.filepathChanged.emit()
        
    def getWidth(self): return self._width        
    def setWidth(self,width):
        if width != self._width:
            self._width = width
            self.widthChanged.emit()
            
    def getHeight(self): return self._height        
    def setHeight(self,height):
        if height != self._height:
            self._height = height
            self.heightChanged.emit()

            
    width = Property(int,getWidth, setWidth, notify=widthChanged)
    height = Property(int, getHeight, setHeight, notify=heightChanged)
    filepath = Property(unicode, getFilepath, setFilepath, notify=filepathChanged)
    modification = Property(bool, getModificationChanged, setModificationChanged, notify=modificationChanged)
