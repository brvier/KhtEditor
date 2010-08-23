#!/usr/bin/python
# -*- coding: utf-8 -*-

#KhtEditor Setup File

from distutils.core import setup

setup(name='KhtEditor',
      version='0.0.2',
      license='GNU GPLv3',
      description='A source code editor designed for Maemo and Meego devices, support Scripts and Plugins.',
      author='Benoît HERVIER',
      author_email='khertan@khertan.net',
      url='http://www.khertan.net/khteditor',
      packages= ['khteditor', 'khteditor/plugins', 'khteditor/syntax'],
      package_data = {'khteditor': ['icons/*.png']},
      data_files=[('/usr/share/dbus-1/services', ['khteditor.service']),
                  ('/usr/share/applications/hildon/', ['khteditor.desktop']),
                  ('/usr/share/pixmaps', ['khteditor.png'])],
      scripts=['khteditor_launch.py'],

     )

