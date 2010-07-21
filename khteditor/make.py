#!/usr/bin/python
# -*- coding: utf-8 -*-
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published
## by the Free Software Foundation; version 2 only.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
import pypackager
import os

if __name__ == "__main__":
    try:
        os.chdir(os.path.dirname(sys.argv[0]))
    except:
        pass

    p=pypackager.PyPackager("khteditor")
    p.version='0.0.1'
    p.buildversion='1'
    p.display_name='KhtEditor'
    p.description="KhtEditor is a source code editor specially designed for devices running Maemo and Meego Handset."
    p.author="Benoît HERVIER"
    p.maintainer="Khertan"
    p.email="khertan@khertan.net"
    p.depends = "python2.5-qt4-gui,python2.5-qt4-core, python2.5-qt4-maemo5"
    p.suggests = "pylint"
    p.section="user/development"
    p.arch="armel"
    p.urgency="low"
    p.bugtracker='http://khertan.net/flyspray/index.php?project=7'
    p.distribution="fremantle"
    p.repository="extras-devel"
    p.icon='khteditor.png'
    p["/usr/bin"] = ["khteditor",]
    p["/usr/share/dbus-1/services"] = ["khteditor.service",]
    p["/usr/share/pixmaps"] = ["khteditor.png",]
    p["/usr/share/applications/hildon"] = ["khteditor.desktop",]
    files = [ "khteditor.py",
                              "editor.py",
                              "editor_window.py",
                              "plugins.py",
                              "main.py",
                              "welcome_window.py",
                              "recent_files.py",
                              "snippets.py",
                              ]

    #Syntax
    for root, dirs, fs in os.walk('/home/user/MyDocs/Projects/khteditor/syntax'):
      for f in fs:
        print os.path.basename(f)
        files.append('syntax/'+os.path.basename(f))
    print files

    #Plugins
    for root, dirs, fs in os.walk('/home/user/MyDocs/Projects/khteditor/plugins'):
      for f in fs:
        print os.path.basename(f)
        files.append('plugins/'+os.path.basename(f))
    print files

    #Snippets
    for root, dirs, fs in os.walk('/home/user/MyDocs/Projects/khteditor/snippets'):
      for f in fs:
        print os.path.basename(f)
        files.append('snippets/'+os.path.basename(f))
    print files

    #Icon
    for root, dirs, fs in os.walk('/home/user/MyDocs/Projects/khteditor/icons'):
      for f in fs:
        print os.path.basename(f)
        files.append('icons/'+os.path.basename(f))
    print files

    p["/opt/khteditor"] = files

    p.postinstall = """#!/bin/sh
chmod +x /usr/bin/khteditor
python -m compileall /home/opt/khteditor"""

    p.changelog="""First Release
"""

#print p.generate(build_binary=False,build_src=True)
print p.generate(build_binary=False,build_src=True)
