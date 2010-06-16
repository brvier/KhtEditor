from PyQt4.QtGui import QTextEdit
from PyQt4.QtCore import Qt,QThread,QProcess,QRegExp,SIGNAL,QString
from plugins import Plugin
import re
#from pylint import lint
#import pylint.lint

class PyLint_Plugin(Plugin):
    capabilities = ['afterFileSave']
    thread = None
    
    def do_afterFileSave(self, parent):
        '''Lauch the PyLint syntax check QThread after a save'''
        self.parent = parent
        print 'FilePath : ',str(parent.filename)
        self.thread = PyLint_Worker(str(parent.filename))
        print 'now start the pylint thread'
        self.parent.connect(self.thread,SIGNAL("hilighterror ( QString,int,QString )"),self.parent.hilighterror)
        self.thread.start()
                
class PyLint_Worker(QThread):
    '''The QThread doing the pylint check'''
    
    def __init__(self,filepath):
        super(PyLint_Worker,self).__init__()
        self.filepath = filepath
        self.stopped = True
        self.completed = False
        
    def run(self):
        print 'thread started'
        self.stopped = False
        result = self.check()
        print 'results :',result
        if result != None:        
            result = QString(result)
            regex = QRegExp('(\w):\s*(\d+):?\s([\w ]*)')
            pos = 0
            while True:
                pos = regex.indexIn(result,pos)
                if pos<0:
                    break            
                self.emit(Qt.SIGNAL('hilighterror(QString,int,QString)',regex.cap(1),regex.cap(2).toInt(),regex.cap(3)))
                pos = pos + regex.matchedLength()
#        while ((pos = rx.indexIn(str, pos)) != -1) {
#     list << rx.cap(1);
#     pos += rx.matchedLength();}
        self.completed = True
        self.stop()
        
#        self.emit(Qt.SIGNAL('finished(bool)',self.completed))
        
    def stop(self):
        print 'Thread stopped'
        self.stopped = True
        
    def check(self):
        print 'starting check !'
        lint = QProcess()
        lint.start("pylint", [self.filepath,])
        if not(lint.waitForStarted()):
            return None
       
        if not(lint.waitForFinished()):
            return None
    
        return lint.readAll()