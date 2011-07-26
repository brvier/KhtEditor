#!/usr/bin/python
# -*- coding: utf-8 -*-

"""KhtEditor a source code editor by Khertan"""

import khteditor
import sys

if __name__ == '__main__':
    print dir(khteditor)

    sys.exit(khteditor.KhtEditor().exec_())

