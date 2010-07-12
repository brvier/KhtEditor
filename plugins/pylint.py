#PYLINT:W:Unused import QThread
#PYLINT:W:Unused import Qt
#PYLINT:C:Comma not followed by a space
#PYLINT:C:Missing docstring
from PyQt4.QtCore import Qt,QThread,QProcess,QRegExp,SIGNAL,QString,QObject
from PyQt4.QtGui import QColor,QTextEdit,QTextFormat,QAction,QIcon
from plugins import Plugin
import re
import os.path

class PyLint_Plugin(Plugin, QObject):
    capabilities = ['toolbarHook']
    thread = None
    
    def do_toolbarHook(self,parent):
        self.parent = parent
        
        #Keep a references to prevent gc 
        #deleting our callback methode
        try:
            self.parent.plugins_ref.append(self)
        except:
            self.parent.plugins_ref = [self,]
            
        icon = QIcon('/home/opt/khteditor/icons/tb_pylint.png')
        print 'test'
        self.parent.tb_pylint = QAction(icon, 'PyLint', self.parent)          
#PYLINT:C:Line too long 
        self.connect(self.parent.tb_pylint, SIGNAL('triggered()'), self.do_pylint)
        self.parent.toolbar.addAction(self.parent.tb_pylint)
        
    def do_pylint(self):
        print 'do_pylint'

        #ask for save if unsaved
        self.parent.editor.closeEvent()

        self.pylintProc = QProcess()

#PYLINT:C:Line too long 
        self.pylintProc.setProcessChannelMode(QProcess.MergedChannels)
        self.pylintProc.setWorkingDirectory(os.path.dirname(str(self.parent.editor.filename)))
        self.pylintProc.setReadChannel(QProcess.StandardOutput)
#PYLINT:C:Line too long 

        self.connect(self.pylintProc, SIGNAL('finished()'), self.handleStdout)
        self.connect(self.pylintProc, SIGNAL('readyReadStandardOutput()'), self.handleStdout)
        self.connect(self.pylintProc, SIGNAL('readyReadStandardError()'), self.handleStderr)
        if (self.pylintProc.start("pylint", [self.parent.editor.filename,])):
            print 'Cannot start process'
        self.pylintProc.waitForStarted()
        
    def handleStdout(self):
        """
        Private slot to handle the readyReadStdout signal of the pylint process.
        """
        while self.pylintProc and self.pylintProc.canReadLine():
            result = self.pylintProc.readLine()
            if result != None:        
                result = QString(result)
                regex = QRegExp('(\w):\s*(\d+):?\s([\w ]*)')
                pos = 0
                inserted_line = 0
                while True:
                    pos = regex.indexIn(result,pos)
                    if pos<0:
                        break
                    line = int(regex.cap(2))
                    block = self.parent.editor.document().findBlockByLineNumber((line-2)+inserted_line)
                    if not (block.text().startsWith('#PYLINT:')):                    
                        block = self.parent.editor.document().findBlockByLineNumber((line-1)+inserted_line)
                        cursor = self.parent.editor.textCursor() 
                        cursor.setPosition(block.position())
                        
                        #Hilgight background
#PYLINT:C:Line too long 
#                        _color = QColor()
#                        _color.setNamedColor('red')
#PYLINT:C:Line too long 
#                        _color.lighter(160)
#                        _selection = QTextEdit.ExtraSelection()
#                        _selection.format.setBackground(_color)
#                        _selection.format.setProperty(QTextFormat.FullWidthSelection, True)       
#                        _selection.cursor = cursor
#                        _selection.cursor.clearSelection()
#                        self.parent.extraSelections().append(_selection)                        
                        cursor.insertText("#PYLINT:"+regex.cap(1)+':'+regex.cap(3)+'\n')
                        inserted_line=inserted_line+1
            
                    pos = pos + regex.matchedLength()

    def handleStderr(self):
        """
        Private slot to handle the readyReadStderr signal of the pylint process.
        """
        print 'error stderr'