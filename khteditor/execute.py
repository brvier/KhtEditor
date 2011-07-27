from PySide.QtCore import Qt, QProcess, Slot
from PySide.QtGui import QMainWindow, QPlainTextEdit, \
                         QScrollArea, QFrame

#Try import QtMaemo5
try:
    from PySide import QtMaemo5
    print '%s loaded' % QtMaemo5.__name__
    from PySide.QtGui import QAbstractKineticScroller
except:
    print 'PySide QtMaemo5 cannot be loaded'

class KhtExecute(QMainWindow):
    def __init__(self,parent=None,command=None):
        self._command = command
        QMainWindow.__init__(self,parent)
        try:
            self.setAttribute(Qt.WA_Maemo5AutoOrientation, True)
#            self.setAttribute(Qt.WA_Maemo5StackedWindow, True)
        except:
            #Resize window if not maemo
            self.resize(400, 400)

        self.area =  QScrollArea(self)
        try:
            scroller = self.area.property("kineticScroller")
            if scroller == None:
                raise StandardError("No QtMaemo5")
            self._logs = QPlainTextEdit(self.area)
            scroller.setEnabled(True)
            scroller.setOvershootPolicy(QAbstractKineticScroller.OvershootAlwaysOff)
            self.area.setWidgetResizable(True)
            self.area.setFrameStyle(QFrame.NoFrame)
            self.area.setViewportMargins(0,0,0,0)
            self.area.setContentsMargins(0,0,0,0)
            self.area.setWidget(self._logs)
            self.setCentralWidget(self.area)
        except Exception, err:
            print err
            self._logs = QPlainTextEdit(self)
            self.area.close()
            self.area.destroy()
            del self.area

            self.setCentralWidget(self._logs)

        self._logs.setReadOnly(True)

        self._processLog = QProcess()
        self._processLog.readyReadStandardOutput.connect(self._readLog)
        
        self._processLog.start(self._command)

    @Slot()
    def _readLog(self):
        while self._processLog.canReadLine():
            self._logs.appendPlainText(unicode(self._processLog.readLine()))
 
if __name__ == "__main__":
    import sys
    from PySide.QtGui import QApplication
    app = QApplication(sys.argv)
    win = KhtExecute(command='python -u %s' % __file__)
    win.show()
    sys.exit(app.exec_())