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
import khteditor

if __name__ == "__main__":
    try:
        os.chdir(os.path.dirname(sys.argv[0]))
    except:
        pass

    p=pypackager.PyPackager("khteditor")
    p.version=khteditor.__version__
    p.buildversion='1'
    p.display_name='KhtEditor'
    p.description="KhtEditor is a source code editor specially designed for devices running Maemo and Meego Handset."
    p.author="Benoît HERVIER"
    p.maintainer="Khertan"
    p.email="khertan@khertan.net"
    p.depends = "python2.5-qt4-gui,python2.5-qt4-core, python2.5-qt4-maemo5, python2.5-qt4-common, python-pygments"
    p.suggests = "pylint"
    p.section="user/development"
    p.arch="armel"
    p.urgency="low"
    p.bugtracker='http://khertan.net/khteditor/bugs'
    p.distribution="fremantle"
    p.repository="extras-devel"
    p.icon='khteditor.png'
    p["/usr/bin"] = ["khteditor_launch.py",]
    p["/usr/share/dbus-1/services"] = ["khteditor.service",]
    p["/usr/share/pixmaps"] = ["khteditor.png",]
    p["/usr/share/applications/hildon"] = ["khteditor.desktop",]
    files = []
    
    #Src
    for root, dirs, fs in os.walk('/home/user/MyDocs/Projects/khteditor/khteditor'):
      for f in fs:
        #print os.path.basename(root),dirs,f
        prefix = 'khteditor/'
        if os.path.basename(root) != 'khteditor':
            prefix = prefix + os.path.basename(root) + '/'
        files.append(prefix+os.path.basename(f))
    print files

    
    p["/usr/lib/python2.5/site-packages"] = files

    p.postinstall = """#!/bin/sh
chmod +x /usr/bin/khteditor_launch.py
python -m compileall /usr/lib/python2.5/site-packages/khteditor"""

    p.changelog=""" Fix pylint plugin, add qml syntax, and some other minor fixes
"""

print p.generate(build_binary=False,build_src=True)
#print p.generate(build_binary=True,build_src=True)
