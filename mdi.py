import sys
import welcome_window
from PyQt4 import QtCore, QtGui

class KWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(KWindow, self).__init__(parent)


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    window1 = KWindow(None)
    window1.resize(800, 480)
    window1.setWindowTitle(window1.tr("Window 1"))
    window1.show()
    window2 = KWindow(None)
    window2.resize(800, 480)
    window2.show()
    window2.setWindowTitle(window2.tr("Window 2"))
    sys.exit(app.exec_())
