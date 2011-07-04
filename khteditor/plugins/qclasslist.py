#!/usr/bin/env python

"""PyLint Plugin : A KhtEditor plugin to lint current source code and
   And display the result"""
                        
from PySide.QtCore import Qt, \
                         QObject, \
                         Slot

from PySide.QtGui import QMainWindow, \
                        QPlainTextEdit

#try:                        
#    import PyQt4.QtMaemo5 #Not really unused as it s import to Qt
#    isMAEMO = True
#except:
#    isMAEMO = False
    
try:
    from plugins_api import Plugin
except:
    from khteditor.plugins.plugins_api import Plugin
        
import sys
import re
           
class ResultWin(QMainWindow):
    """ Window use to display pylint results """
    
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.parent = parent
        try:
            self.setAttribute(Qt.WA_Maemo5AutoOrientation, True)
        except AttributeError:
            pass
        self.qclasses = QPlainTextEdit()        
        self.setCentralWidget(self.qclasses)
                         
class PyQClassList(Plugin, QObject):
    """ PyLint Plugin """
    capabilities = ['toolbarHook']
    __version__ = '0.5'
    thread = None
    
    def __init__(self):
        QObject.__init__(self,parent=None)
        
    def do_toolbarHook(self, widget):
        self.parent = widget.parent() #Get the editor_window object
        widget.addAction('QClass',self.do_parse)

    @Slot()
    def do_parse(self):        
        """ Parse the file to list QtClass """
        import os.path
        print 'QClass do parse called'
        self.win = ResultWin()
        self.win.setWindowTitle("List of QtClass :" \
            + os.path.basename(str(self.parent.editor.filename)))
        self.win.show()
        try:
            self.win.setAttribute(Qt.WA_Maemo5ShowProgressIndicator, True)
        except AttributeError:
            pass
        f = open(self.parent.editor.filename)
        s = f.read()
        f.close()
        
        regex = re.compile('Q\w*')
        dupelist = regex.findall(s)

        unilist = {}
        for item in dupelist:
            try:
                unilist[item]=1
            except TypeError:
                pass                

        unilist = unilist.keys()

        #pre import 
        import PyQt4
        import glob
        import os.path

        #discover of existing qt modules
        mods_paths = glob.glob(os.path.join(PyQt4.__path__[0] , '*'))
        mods = []
        for mod_path in mods_paths:
            mods.append(os.path.basename(os.path.splitext(mod_path)[0]))

        #Import all know qt module
        for mod in mods:
            try:
                print __import__('PyQt4.'+mod, None, None, [''])
            except:
                mods.remove(mod)

        #Put class in right module list
        mods_class = {}
        for aclass in unilist:
            for mod in mods:
                try:
                    if aclass in dir(eval('PyQt4.'+mod)):
                        try:
                            mods_class[mod].append(aclass)
                        except:
                            mods_class[mod] = [aclass, ]
                        continue
                except:
                    pass

        text = ''
        for mod in mods:
            if mod in mods_class:
                text = text + '\nfrom PyQt4.' + mod + ' import ' + (', \\\n    '.join(mods_class[mod]))
                        
        self.win.qclasses.setPlainText(text)

        try:
            self.win.setAttribute(Qt.WA_Maemo5ShowProgressIndicator, False)
        except AttributeError:
            pass
