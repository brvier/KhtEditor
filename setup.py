#!/usr/bin/python
# -*- coding: utf-8 -*-

#KhtEditor Setup File

from distutils.core import setup

setup(name='KhtEditor',
      version='0.0.1',
      licence='GPLv2',
      description='A source code editor designed for Maemo and Meego devices, support Scripts and Plugins.',
      author='Benoît HERVIER',
      author_email='khertan@khertan.net',
      url='http://www.khertan.net/khteditor',
      packages=['khteditor', 'khteditor/plugins', 'khteditor/syntax', 'khteditor/snippets', 'khteditor/icons'],
      data_files=[('/usr/share/dbus-1/services', ['khteditor.service']),
                  ('/usr/share/applications/hildon/', ['khteditor.desktop']),
                  ('/usr/share/pixmaps', ['khteditor.png']),
                  ('/usr/bin', ['khteditor.py'])],
     )

