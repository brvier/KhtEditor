#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""KhtEditor a source code editor by Khertan : Init"""

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

__version__ = '1.0.4'

import os
import sys
import welcome_window
from PyQt4.QtCore import Qt , QSettings, QUrl
from PyQt4.QtGui import QMainWindow, QScrollArea, \
                        QWidget, QSizePolicy, \
                        QVBoxLayout, QLabel, \
                        QIcon, QPushButton, \
                        QHBoxLayout, \
                        QDesktopServices, \
                        QApplication, QMessageBox

import editor_window
from recent_files import RecentFiles

import settings

#Here is the installation of the hook. Each time a untrapped/unmanaged exception will
#happen my_excepthook will be called.
def install_excepthook(app_name,app_version):
    '''Install exception hook for the bug reporter'''
    APP_NAME = 'KhtEditor'
    APP_VERSION = __version__

    def write_report(error):
        import pickle
        filename = os.path.join(os.path.join(os.path.expanduser("~"),'.khteditor_crash_report'))
        output = open(filename, 'wb')
        pickle.dump(error, output)
        output.close()

    def my_excepthook(exctype, value, tb):
        #traceback give us all the errors information message like the method, file line ... everything like
        #we have in the python interpreter
        import traceback
        s = ''.join(traceback.format_exception(exctype, value, tb))
        print 'Except hook called : %s' % (s)
        formatted_text = "%s Version %s\nTrace : %s\nComments : " % (APP_NAME, APP_VERSION, s)
        write_report(formatted_text)

    sys.excepthook = my_excepthook

class KhtEditorAbout( QMainWindow):
    '''About Window'''
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)
        self.parent = parent

        self.settings =  QSettings()

        try:
            self.setAttribute(Qt.WA_Maemo5AutoOrientation, True)
            self.setAttribute(Qt.WA_Maemo5StackedWindow, True)
            isMAEMO = True
        except:
            isMAEMO = False
        self.setWindowTitle("KhtEditor About")

        #Resize window if not maemo
        if not isMAEMO:
            self.resize(800, 600)

        aboutScrollArea =  QScrollArea(self)
        aboutScrollArea.setWidgetResizable(True)
        awidget =  QWidget(aboutScrollArea)
        awidget.setMinimumSize(480,800)
        awidget.setSizePolicy(  QSizePolicy.Expanding,  QSizePolicy.Expanding)
        aboutScrollArea.setSizePolicy(  QSizePolicy.Expanding,  QSizePolicy.Expanding)
        #Kinetic scroller is available on Maemo and should be on meego
        try:
            scroller = aboutScrollArea.property("kineticScroller") #.toPyObject()
            scroller.setEnabled(True)
        except:
            pass

        aboutLayout =  QVBoxLayout(awidget)

        aboutIcon =  QLabel()
        aboutIcon.setPixmap( QIcon.fromTheme('khteditor').pixmap(128,128))
        aboutIcon.setAlignment( Qt.AlignCenter or Qt.AlignHCenter )
        aboutIcon.resize(128,128)
        aboutLayout.addWidget(aboutIcon)

        aboutLabel =  QLabel('''<center><b>KhtEditor</b> %s
                                   <br><br>A source code editor designed for ease of use on small screen
                                   <br>Licenced under GPLv3
                                   <br>By Beno&icirc;t HERVIER (Khertan)
                                   <br><br><br><b>Bugtracker : </b>http://khertan.net/khteditor:bugs
                                   <br><b>Sources : </b>http://gitorious.org/khteditor
                                   <br><b>Www : </b>http://khertan.net/khteditor
                                   <br><br><b>Thanks to :</b>
                                   <br>achipa on #pyqt
                                   <br>ddoodie on #pyqt
                                   <br>Attila77 on talk.maemo.org
                                   <br>Sebastian Lauwers for help on regex
                                   <br><br>
                                   </center>''' % __version__)

        aboutLayout.addWidget(aboutLabel)
        self.bugtracker_button =  QPushButton('BugTracker')
        self.bugtracker_button.clicked.connect(self.open_bugtracker)
        self.website_button =  QPushButton('Website')
        self.website_button.clicked.connect(self.open_website)
        awidget2 =  QWidget()
        buttonLayout =  QHBoxLayout(awidget2)
        buttonLayout.addWidget(self.bugtracker_button)
        buttonLayout.addWidget(self.website_button)
        aboutLayout.addWidget(awidget2)

        awidget.setLayout(aboutLayout)
        aboutScrollArea.setWidget(awidget)
        self.setCentralWidget(aboutScrollArea)
        self.show()

    def open_website(self):
         QDesktopServices.openUrl( QUrl('http://khertan.net/khteditor'))
    def open_bugtracker(self):
         QDesktopServices.openUrl( QUrl('http://khertan.net/khteditor/bugs'))


class KhtEditor:
    def __init__(self):
        self.window_list = []
        self.version = __version__

        self.app =  QApplication(sys.argv)
        self.app.setOrganizationName("Khertan Software")
        self.app.setOrganizationDomain("khertan.net")
        self.app.setApplicationName("KhtEditor")

        install_excepthook(self.app.applicationName(),self.version)

        self.last_know_path='/home/user/MyDocs'
        self.run()

    def crash_report(self):
        if os.path.isfile(os.path.join(os.path.join(os.path.expanduser("~"),'.khteditor_crash_report'))):
            import urllib2
            import urllib
            import pickle
            if (( QMessageBox.question(None,
                "KhtEditor Crash Report",
                "An error occur on KhtEditor in the previous launch. Report this bug on the bug tracker ?",
                QMessageBox.Yes| QMessageBox.Close)) ==  QMessageBox.Yes):
                url = 'http://khertan.net/report.php' # write ur URL here
                try:
                    filename = os.path.join(os.path.join(os.path.expanduser("~"),'.khteditor_crash_report'))
                    output = open(filename, 'rb')
                    error = pickle.load(output)
                    output.close()

                    values = {
                          'project' : 'khteditor',
                          'version': __version__,
                          'description':error,
                      }

                    data = urllib.urlencode(values)
                    req = urllib2.Request(url, data)
                    response = urllib2.urlopen(req)
                    the_page = response.read()
                except Exception, detail:
                    print detail
                    QMessageBox.question(None,
                    "KhtEditor Crash Report",
                    "An error occur during the report : %s" % detail,
                    QMessageBox.Close)
                    return False

                if 'Your report have been successfully stored' in the_page:
                    QMessageBox.question(None,
                    "KhtEditor Crash Report",
                    "%s" % the_page,
                    QMessageBox.Close)
                    return True
                else:
                    print 'page:',the_page
                    QMessageBox.question(None,
                    "KhtEditor Crash Report",
                    "%s" % the_page,
                    QMessageBox.Close)
                    return False
            try:
                os.remove(os.path.join(os.path.join(os.path.expanduser("~"),'.khteditor_crash_report')))
            except:
                pass

    def run(self):
        """
            Run method
        """

        window = welcome_window.WelcomeWindow(self)
        window.show()
        self.crash_report()

        for arg in self.app.argv()[1:]:
            path = os.path.abspath(arg)
            if os.path.isfile(unicode(path)):
                editor_win=editor_window.Window(self)
                self.window_list.append(editor_win)
                editor_win.loadFile(unicode(path))
                editor_win.show()
                self.last_know_path=os.path.dirname(unicode(path))
                RecentFiles().append(unicode(path))

        sys.exit(self.app.exec_())

    def about(self,widget):
        self.aboutWin = KhtEditorAbout(widget)

    def newFile(self):
        """
            Create a new editor window
        """

        editor_win = editor_window.Window(self)
        editor_win.show()
        self.window_list.append(editor_win)

    def openFile(self):
        """
            Create a new editor window and open selected file
        """
        editor_win=editor_window.Window(self)
        editor_win.show()
        filename = editor_win.openFile(self.last_know_path)
        if not (filename == ''):
            self.window_list.append(editor_win)
            RecentFiles().append(filename)
            self.last_know_path=os.path.dirname(unicode(filename))
#        else:
#          editor_win.destroy()

    def openRecentFile(self, path):
        """
            Create a new editor window and open a recent file
        """
        editor_win=editor_window.Window(self)
        self.window_list.append(editor_win)
        editor_win.show()
        try:
            editor_win.loadFile(path.valueText())
            RecentFiles().append(path.valueText())
            self.last_know_path=os.path.dirname(unicode(path.valueText()))
        except:
            editor_win.loadFile(path.text())
            RecentFiles().append(path.text())
            self.last_know_path=os.path.dirname(unicode(path.text()))


    def showPrefs(self,win):
        """
            Instantiate the prefs window and show it
        """

        self.khtsettings = settings.KhtSettings(win)
        self.khtsettings.show()

if __name__ == '__main__':
    KhtEditor()