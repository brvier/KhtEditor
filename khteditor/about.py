from PySide.QtGui import QMainWindow, QHBoxLayout, QSizePolicy, \
    QVBoxLayout, QDesktopServices, QScrollArea, QPushButton, \
    QLabel, QWidget, QIcon
from PySide.QtCore import Qt, QUrl, QSettings, Slot

try:
    from PySide.QtMaemo5 import *
except ImportError:
    print 'QtMaemo5 Not available'

from khteditor import __version__
import os

class QAboutWin(QMainWindow):

    '''About Window'''


    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.parent = parenty

        self.settings = QSettings()

        try:  # Preferences not set yet
            self.setAttribute(Qt.WA_Maemo5AutoOrientation, True)
            self.setAttribute(Qt.WA_Maemo5StackedWindow, True)
        except:
            pass

        self.setWindowTitle(self.tr('KhtEditor About'))

        try:
            aboutScrollArea = QScrollArea(self)
            aboutScrollArea.setWidgetResizable(True)
            awidget = QWidget(aboutScrollArea)
            awidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            aboutScrollArea.setSizePolicy(QSizePolicy.Expanding,
                    QSizePolicy.Expanding)

        # Kinetic scroller is available on Maemo and should be on meego

            try:
                scroller = aboutScrollArea.property('kineticScroller')
                scroller.setEnabled(True)
            except:
                aboutScrollArea.close()
                aboutScrollArea.destroy()
                del aboutScrollArea

            aboutLayout = QVBoxLayout(awidget)
        except:
            awidget = QWidget(self)
            aboutLayout = QVBoxLayout(awidget)

        aboutIcon = QLabel()
        icon = QIcon.fromTheme('khteditor').pixmap(128, 128)
        print icon
        if not icon:
            icon = QIcon(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'icons', 'khteditor.png')).pixmap(128, 128)
        aboutIcon.setPixmap(icon)

        aboutIcon.setAlignment(Qt.AlignCenter or Qt.AlignHCenter)
        aboutIcon.resize(128, 128)
        aboutLayout.addWidget(aboutIcon)


        aboutLabel =  QLabel('''<center><b>KhtEditor</b> %s
                                   <br><br>A source code editor designed for ease of use on small screen
                                   <br>Licenced under GPLv3
                                   <br>By Beno&icirc;t HERVIER (Khertan)
                                   <br><br><br><b>Bugtracker : </b>http://khertan.net/khteditor:bugs
                                   <br><b>Sources : </b>http://gitorious.org/khteditor
                                   <br><b>www : </b>http://khertan.net/khteditor
                                   <br><br><b>Thanks to :</b>
                                   <br>achipa on #pyqt
                                   <br>ddoodie on #pyqt
                                   <br>Attila77 on talk.maemo.org
                                   <br>Sebastian Lauwers for help on regex
                                   <br><br>
                                   </center>''' % __version__)

        aboutLayout.addWidget(aboutLabel)
        self.bugtracker_button = QPushButton(self.tr('BugTracker'))
        self.bugtracker_button.clicked.connect(self.open_bugtracker)
        self.website_button = QPushButton(self.tr('Website'))
        self.website_button.clicked.connect(self.open_website)
        awidget2 = QWidget()
        buttonLayout = QHBoxLayout(awidget2)
        buttonLayout.addWidget(self.bugtracker_button)
        buttonLayout.addWidget(self.website_button)
        aboutLayout.addWidget(awidget2)
        awidget.resize(-1,-1)

        try:
            awidget.setLayout(aboutLayout)
            aboutScrollArea.setWidget(awidget)
            self.setCentralWidget(aboutScrollArea)
        except Exception, err:
            print "DEBUG:", err
            self.setCentralWidget(awidget)

        self.show()

    @Slot()
    def open_website(self):
        QDesktopServices.openUrl(QUrl('http://khertan.net/khteditor'))

    @Slot()
    def open_bugtracker(self):
        QDesktopServices.openUrl(QUrl('http://khertan.net/khteditor/bugs'))
