#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""KhtEditor a source code editor by Khertan"""

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

import khteditor

if __name__ == '__main__':
    khteditor.KhtEditor()
