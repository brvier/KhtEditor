#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""KhtEditor a source code editor by Khertan : Welcome Window"""

VERSION = '0.0.2'

import os
import sys
import welcome_window
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
import editor_window
from recent_files import RecentFiles
import khteditor
import settings

class KhtEditor:
    def __init__(self):
      self.window_list = []
      self.version = VERSION

      self.app = QtGui.QApplication(sys.argv)
      self.app.setOrganizationName("Khertan Software")
      self.app.setOrganizationDomain("khertan.net")
      self.app.setApplicationName("KhtEditor")
      
      self.last_know_path='/home/user/MyDocs'
      self.run()

    def run(self):
#      settings = QtCore.QSettings()
#      self.recentFiles = settings.value("RecentFiles").toStringList()

      window = welcome_window.WelcomeWindow(self)
      window.show()
      
      for arg in self.app.argv()[1:]:
          path = os.path.abspath(arg)
          if os.path.isfile(path):
              editor_win=editor_window.Window(self)
              self.window_list.append(editor_win)
              editor_win.loadFile(QtCore.QString(path))
              editor_win.show()
              RecentFiles().append(QtCore.QString(path))

      sys.exit(self.app.exec_())
      
    def about(self,widget):
        #QtGui.QMessageBox.about(widget, ("About KhtEditor"),
        #        ("<p><b>KhtEditor</b> is a source code editor "
        #                "Mainly designed for Maemo and Meego.</p>"))
        aboutWin = QtGui.QMainWindow(widget)
        aboutWin.setAttribute(Qt.WA_Maemo5StackedWindow, True)
        aboutWin.setAttribute(Qt.WA_Maemo5AutoOrientation, True)

        aboutScrollArea = QtGui.QScrollArea(aboutWin)
        aboutScrollArea.setWidgetResizable(True)
        awidget = QtGui.QWidget(aboutScrollArea)
        awidget.setMinimumSize(480,600)
        awidget.setSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        aboutScrollArea.setSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        scroller = aboutScrollArea.property("kineticScroller").toPyObject()
        scroller.setEnabled(True)

        aboutLayout = QtGui.QVBoxLayout(awidget)
        
        aboutIcon = QtGui.QLabel()
        aboutIcon.setPixmap(QtGui.QPixmap(os.path.join(khteditor.__path__[0],'icons','khteditor.png')).scaledToHeight(128))
        aboutIcon.setAlignment( Qt.AlignCenter or Qt.AlignHCenter )
        aboutIcon.resize(140,140)
        aboutLayout.addWidget(aboutIcon)
        
        aboutLabel = QtGui.QLabel('''<center><b>KhtEditor</b> %s
                                   <br><br>A source code editor designed for ease of use on small screen
                                   <br>Licenced under GPLv3
                                   <br>By Beno&icirc;t HERVIER (Khertan) 
                                   <br><br><br><b>Bugtracker : </b>http://khertan.net/flyspray
                                   <br><b>Sources : </b>http://gitorious.org/khteditor                                   
                                   <br><br><b>Thanks to :</b>
                                   <br>achipa on #pyqt
                                   <br>ddoodie on #pyqt
                                   <br>Attila77 on talk.maemo.org
                                   
                                   </center>''' % self.version)
        aboutLayout.addWidget(aboutLabel)

        awidget.setLayout(aboutLayout)
        aboutScrollArea.setWidget(awidget)

        aboutWin.setWindowTitle('About KhtEditor')
        aboutWin.setCentralWidget(aboutScrollArea)
        aboutWin.show()
        
    def newFile(self):
        editor_win = editor_window.Window(self)
        editor_win.show()
        self.window_list.append(editor_win)

    def openFile(self, path=QtCore.QString()):
            editor_win=editor_window.Window(self)
            filename = editor_win.openFile(self.last_know_path)
            if not filename.isEmpty():
              editor_win.show()
              self.window_list.append(editor_win)
              RecentFiles().append(filename)
              self.last_know_path=QtCore.QString(os.path.dirname(str(filename)))
            else:
              editor_win.destroy()

    def openRecentFile(self, path=QtCore.QString()):
        editor_win=editor_window.Window(self)
        self.window_list.append(editor_win)
        editor_win.loadFile(path.valueText())
        editor_win.show()
        RecentFiles().append(path.valueText())
        self.last_know_path=QtCore.QString(os.path.dirname(str(path))) 
            
    def showPrefs(self,win):
        self.khtsettings = settings.KhtSettings(win)
        self.khtsettings.show()

if __name__ == '__main__':
    KhtEditor()
