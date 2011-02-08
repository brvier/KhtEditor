#!/usr/bin/python
# -*- coding: utf-8 -*-

#KhtEditor Setup File
import khteditor
import imp
import sys
reload(sys).setdefaultencoding("UTF-8")

try:
    from sdist_maemo import sdist_maemo as _sdist_maemo
except:
    _sdist_maemo = None
    print 'sdist_maemo command not available'

from distutils.core import setup

#Remove pyc and pyo file
import glob,os
for fpath in glob.glob('*/*.py[c|o]'):
    os.remove(fpath)
    
setup(name='khteditor',
      version=khteditor.__version__,
      license='GNU GPLv3',
      description='A source code editor designed for Maemo and Meego devices, support Scripts and Plugins.',
      author='Benoît HERVIER',
      author_email='khertan@khertan.net',
      url='http://www.khertan.net/khteditor',
      requires=['pygments','pyqt4'],
      packages= ['khteditor', 'khteditor/plugins', 'khteditor/syntax'],
      package_data = {'khteditor': ['icons/*.png'],
                      'khteditor': ['syntax/*.xml']},
      data_files=[('/usr/share/dbus-1/services', ['khteditor.service']),
                  ('/usr/share/applications/hildon/', ['khteditor.desktop']),
                  ('/usr/share/pixmaps', ['khteditor.png']),
                  ('/usr/share/icons/hicolor/128x128/apps', ['khteditor.png']),
                  ],
      scripts=['khteditor_launch.py'],
      cmdclass={'sdist_maemo': _sdist_maemo},      
      options = { 'sdist_maemo':{
      'buildversion':'1',
      'depends':'python2.5-qt4-gui,python2.5-qt4-core, python2.5-qt4-maemo5, python2.5-qt4-common, python-pygments',
      'suggests':'pylint',
      'XSBC_Bugtracker':'http://khertan.net/khteditor:bugs',
      'XB_Maemo_Display_Name':'KhtEditor',
      'XB_Maemo_Icon_26':'khteditor.png',
      'section':'user/development',
      'changelog':'* Fix bug #60 (QSetting return unicode instead of a list)\n* Fix bug #58 (Error is now managed)\n* Optimize import by avoiding * import\n* add QClassList plugin which try to generate import of QtClass\n* switch to new signal style\n* Fix autoindent plugin',
      'architecture':'any',
      'postinst':"""#!/bin/sh
chmod +x /usr/bin/khteditor_launch.py
python -m compileall /usr/lib/python2.5/site-packages/khteditor
""",
      'prere':"""#!/bin/sh
rm -rf /usr/lib/python2.5/site-packages/khteditor/*.pyc""",
      'copyright':'gpl'},
      'bdist_rpm':{
      'requires':'python2.5-qt4-gui,python2.5-qt4-core, python2.5-qt4-maemo5, python2.5-qt4-common, python-pygments',
      'icon':'khteditor.png',
      'group':'Network',}}
     )
