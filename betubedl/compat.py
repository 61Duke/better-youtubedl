# -*- coding: utf-8 -*-
# flake8: noqa
import sys

PYTHON_2 = sys.version_info[0] == 2
PYTHON_3 = sys.version_info[0] == 3

if PYTHON_2:
    from urllib2 import urlopen
    from urlparse import urlparse, parse_qs, unquote
if PYTHON_3:
    from urllib.parse import urlparse, parse_qs, unquote
    from urllib.request import urlopen
