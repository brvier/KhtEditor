#!/usr/bin/python
# -*- coding: utf-8 -*-

#KhtEditor Setup File
import khteditor
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

for fpath in glob.glob('*/plugins/*.py[c|o]'):
    os.remove(fpath)
for fpath in glob.glob('*/syntax/*.py[c|o]'):
    os.remove(fpath)


setup(name='khteditor',
      version=khteditor.__version__,
      license='GNU GPLv3',
      description='A source code editor.',
      long_description="A source code editor designed for Maemo and Meego devices, support Scripts and Plugins..",
      author='Benoît HERVIER',
      author_email='khertan@khertan.net',
      maintainer=u'Benoît HERVIER',
      maintainer_email='khertan@khertan.net',
      url='http://www.khertan.net/khteditor',
      requires=['pyside','pyflakes'],
      #suggests=['pylint', 'python-pygments'],
      packages= ['khteditor', 'khteditor/plugins', 'khteditor/syntax'],
      package_data = {'khteditor': ['icons/*.png', 'syntax/*.xml', 'qml/*.js', 'qml/*.qml'],},
      data_files=[('/usr/share/dbus-1/services', ['khteditor.service']),
                  ('/usr/share/applications/', ['khteditor.desktop']),
                  ('/usr/share/pixmaps', ['khteditor.png']),
                  ('/usr/share/icons/blanco/80x80/apps', ['khteditor.png']),
                  ],
      scripts=['khteditor_launch.py'],
      cmdclass={'sdist_maemo': _sdist_maemo},
      options = { 'sdist_maemo':{
      'buildversion':'1',
      'depends':'python-pyside.qtdeclarative',
      'suggests':'pylint, python-pygments (>=1.4.0-4), pyflakes',
      'Maemo_Bugtracker':'http://khertan.net/khteditor:bugs',
      'Maemo_Display_Name':'KhtEditor',
      'Maemo_Icon_26':'khteditor.png',
      'Maemo_Flags':'visible',
      'MeeGo_Desktop_Entry_Filename':'/usr/share/applications/installer-extra/khteditor.desktop',
      'section':'user/development',
      'changelog':'* Improve pyflakes plugin, bugs fixes, improve selector, fix generic highlighter',
      'Maemo_Upgrade_Description':'Improve plugin pyflake, bugs fixes, improve selector, fix generic highlighter',
      'architecture':'any',
      'postinst':"""#!/bin/sh
chmod +x /usr/local/bin/khteditor_launch.py
""",
      'copyright':'gpl'},
      'bdist_rpm':{
      'requires':'python-pyside.qtdeclarative, pyflakes',
      'icon':'khteditor.png',
      'group':'Development',}}
     )

