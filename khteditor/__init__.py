#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""KhtEditor a source code editor by Khertan : Init"""

__version__ = '0.0.9'

import os
import sys
import welcome_window
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
import editor_window
from recent_files import RecentFiles
import khteditor
import settings

#Here is the installation of the hook. Each time a untrapped/unmanaged exception will
#happen my_excepthook will be called.
def install_excepthook(app_name,app_version):

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

class KhtEditor:
    def __init__(self):
      self.window_list = []
      self.version = __version__

      self.app = QtGui.QApplication(sys.argv)
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
            if ((QtGui.QMessageBox.question(None,
                "KhtEditor Crash Report",
                "An error occur on KhtEditor in the previous launch. Report this bug on the bug tracker ?",
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.Close)) == QtGui.QMessageBox.Yes):
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
                    QtGui.QMessageBox.question(None,
                    "KhtEditor Crash Report",
                    "An error occur during the report : %s" % detail,
                    QtGui.QMessageBox.Close)
                    return False

                if 'Your report have been successfully stored' in the_page:
                    QtGui.QMessageBox.question(None,
                    "KhtEditor Crash Report",
                    "%s" % the_page,
                    QtGui.QMessageBox.Close)
                    return True
                else:
                    print 'page:',the_page
                    QtGui.QMessageBox.question(None,
                    "KhtEditor Crash Report",
                    "%s" % the_page,
                    QtGui.QMessageBox.Close)
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
          if os.path.isfile(path):
              editor_win=editor_window.Window(self)
              self.window_list.append(editor_win)
              editor_win.loadFile(QtCore.QString(path))
              editor_win.show()
              self.last_know_path=QtCore.QString(os.path.dirname(str(path)))
              RecentFiles().append(QtCore.QString(path))

        sys.exit(self.app.exec_())
      
    def about(self,widget):
        """
            Display the about dialog
        """
        aboutWin = QtGui.QMainWindow(widget)
        aboutWin.setAttribute(Qt.WA_Maemo5StackedWindow, True)
        aboutWin.setAttribute(Qt.WA_Maemo5AutoOrientation, True)

        aboutScrollArea = QtGui.QScrollArea(aboutWin)
        aboutScrollArea.setWidgetResizable(True)
        awidget = QtGui.QWidget(aboutScrollArea)
        awidget.setMinimumSize(480,800)
        awidget.setSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        aboutScrollArea.setSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        scroller = aboutScrollArea.property("kineticScroller").toPyObject()
        scroller.setEnabled(True)

        aboutLayout = QtGui.QVBoxLayout(awidget)
        
        aboutIcon = QtGui.QLabel()
        aboutIcon.setPixmap(QtGui.QPixmap(os.path.join(khteditor.__path__[0],'icons','khteditor.png')).scaledToHeight(140))
        aboutIcon.setAlignment( Qt.AlignCenter or Qt.AlignHCenter )
        aboutIcon.resize(140,140)
        aboutLayout.addWidget(aboutIcon)
        
        aboutLabel = QtGui.QLabel('''<center><b>KhtEditor</b> %s
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
                                   </center>''' % self.version)
        aboutLayout.addWidget(aboutLabel)

        awidget.setLayout(aboutLayout)
        aboutScrollArea.setWidget(awidget)

        aboutWin.setWindowTitle('About KhtEditor')
        aboutWin.setCentralWidget(aboutScrollArea)
        aboutWin.show()
        
    def newFile(self):
        """
            Create a new editor window
        """
        
        editor_win = editor_window.Window(self)
        editor_win.show()
        self.window_list.append(editor_win)

    def openFile(self, path=QtCore.QString()):
        """
            Create a new editor window and open selected file
        """
        editor_win=editor_window.Window(self)
        editor_win.show()
        filename = editor_win.openFile(self.last_know_path)
        if not filename.isEmpty():
          self.window_list.append(editor_win)
          RecentFiles().append(filename)
          self.last_know_path=QtCore.QString(os.path.dirname(str(filename)))
#        else:           
#          editor_win.destroy()

    def openRecentFile(self, path=QtCore.QString()):
        """
            Create a new editor window and open a recent file
        """
        
        editor_win=editor_window.Window(self)
        self.window_list.append(editor_win)
        editor_win.show()
        editor_win.loadFile(path.valueText())
        RecentFiles().append(path.valueText())
        self.last_know_path=QtCore.QString(os.path.dirname(str(path.valueText()))) 
            
    def showPrefs(self,win):
        """
            Instantiate the prefs window and show it
        """
        
        self.khtsettings = settings.KhtSettings(win)
        self.khtsettings.show()

if __name__ == '__main__':
    KhtEditor()
